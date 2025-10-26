# COMPLETE ERROR RECOVERY MODULE
# Place this file at: core/error_recovery.py

import asyncio
import random
import json
from typing import Dict, Any, Callable, Optional, Coroutine
from datetime import datetime
from pathlib import Path
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class RetryStrategy:
    """Exponential backoff retry strategy for failed API calls"""
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for exponential backoff with jitter"""
        # Exponential backoff: base_delay * (exponential_base ^ attempt)
        delay = self.base_delay * (self.exponential_base ** attempt)
        # Add jitter to prevent thundering herd
        jitter = random.uniform(0, 0.1 * delay)
        total_delay = min(delay + jitter, self.max_delay)
        return total_delay
    
    async def execute_with_retry(
        self,
        coro_func: Callable[..., Coroutine],
        *args,
        **kwargs
    ) -> Any:
        """Execute coroutine with retry logic"""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                print(f"  🔄 Attempt {attempt + 1}/{self.max_retries}")
                result = await coro_func(*args, **kwargs)
                if attempt > 0:
                    print(f"  ✅ Success after {attempt} retries")
                return result
            
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    delay = self.calculate_delay(attempt)
                    print(f"  ❌ Error: {str(e)[:80]}")
                    print(f"  ⏳ Retrying in {delay:.1f}s...")
                    await asyncio.sleep(delay)
                else:
                    print(f"  ❌ Failed after {self.max_retries} attempts")
        
        raise last_error


class ErrorHandler:
    """Comprehensive error handling and recovery system"""
    
    def __init__(self, workspace_dir: str = "workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.error_log_file = self.workspace_dir / ".orchestrator" / "error_log.json"
        self.error_history = []
        self.load_error_history()
    
    def log_error(
        self,
        error: Exception,
        severity: ErrorSeverity,
        context: str,
        recoverable: bool = True,
        recovery_action: Optional[str] = None
    ) -> Dict[str, Any]:
        """Log error with context and recovery information"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "severity": severity.name,
            "context": context,
            "recoverable": recoverable,
            "recovery_action": recovery_action,
            "traceback": self._get_traceback(error)
        }
        
        self.error_history.append(error_entry)
        self._save_error_log()
        
        # Print user-friendly error message
        self._print_error_message(error_entry)
        
        return error_entry
    
    def _get_traceback(self, error: Exception) -> str:
        """Get formatted traceback"""
        import traceback
        return traceback.format_exc()
    
    def _print_error_message(self, error_entry: Dict[str, Any]):
        """Print user-friendly error message"""
        severity = error_entry["severity"]
        context = error_entry["context"]
        message = error_entry["error_message"]
        recoverable = error_entry["recoverable"]
        recovery_action = error_entry.get("recovery_action")
        
        severity_emoji = {
            "LOW": "⚠️",
            "MEDIUM": "⚠️⚠️",
            "HIGH": "❌",
            "CRITICAL": "🔴"
        }
        
        emoji = severity_emoji.get(severity, "⚠️")
        
        print(f"\n{emoji} {severity} ERROR")
        print(f"{'='*60}")
        print(f"Context: {context}")
        print(f"Error: {message}")
        
        if recoverable:
            print(f"Status: ✅ Recoverable")
            if recovery_action:
                print(f"Action: {recovery_action}")
        else:
            print(f"Status: ❌ Critical - Manual intervention required")
        
        print(f"{'='*60}\n")
    
    def _save_error_log(self):
        """Save error log to file"""
        try:
            self.error_log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.error_log_file, 'w') as f:
                json.dump(self.error_history, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save error log: {e}")
    
    def load_error_history(self):
        """Load previous error history if available"""
        if self.error_log_file.exists():
            try:
                with open(self.error_log_file, 'r') as f:
                    self.error_history = json.load(f)
            except Exception as e:
                print(f"⚠️  Could not load error history: {e}")
    
    def get_recovery_suggestion(self, error_type: str) -> str:
        """Get recovery suggestion based on error type"""
        suggestions = {
            "ConnectionError": "Check your internet connection and try again",
            "TimeoutError": "API request timed out. Try reducing model complexity or batch size",
            "AuthenticationError": "API key is invalid or expired. Check your .env file",
            "RateLimitError": "Rate limit exceeded. Wait before making more requests",
            "ValueError": "Invalid parameter or configuration. Check input values",
            "KeyError": "Missing required configuration. Check environment variables",
            "FileNotFoundError": "Required file not found. Check file paths",
            "MemoryError": "Out of memory. Reduce batch size or model size",
            "RuntimeError": "Unexpected runtime error. Check system resources"
        }
        
        return suggestions.get(error_type, "Unknown error. Check logs for details")


class CircuitBreaker:
    """Circuit breaker pattern for API calls - prevents cascading failures"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, coro_func: Callable[..., Coroutine], *args, **kwargs) -> Any:
        """Execute call with circuit breaker protection"""
        if self.state == "OPEN":
            if self._should_attempt_reset():
                print("🔄 Circuit breaker attempting reset (HALF_OPEN)")
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN - API temporarily unavailable")
        
        try:
            result = await coro_func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                print("✅ Circuit breaker reset (CLOSED)")
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.failure_threshold:
                print(f"🔴 Circuit breaker opened after {self.failure_count} failures")
                self.state = "OPEN"
            
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if not self.last_failure_time:
            return True
        
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout