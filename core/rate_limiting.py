# COMPLETE RATE LIMITING AND COST TRACKING MODULE
# Place this file at: core/rate_limiting.py

import asyncio
import time
from typing import Dict, List
from datetime import datetime, timedelta
import json
from pathlib import Path


class RateLimiter:
    """Manages API rate limits and cost tracking across different providers"""
    
    def __init__(self, workspace_dir: str = "workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
        
        # Rate limit configurations (calls per minute)
        self.rate_limits = {
            "openrouter": {"calls_per_minute": 20, "concurrent_requests": 10},
            "groq": {"calls_per_minute": 30, "concurrent_requests": 15},
            "google": {"calls_per_minute": 60, "concurrent_requests": 20}
        }
        
        # Cost tracking (estimates for free tier)
        self.cost_tracking = {
            "openrouter": {"cost_per_1k_tokens": 0},  # Free models
            "groq": {"cost_per_1k_tokens": 0},  # Free tier
            "google": {"cost_per_1k_tokens": 0}  # Free tier
        }
        
        # Request tracking
        self.request_history = {
            "openrouter": [],
            "groq": [],
            "google": []
        }
        
        self.stats_file = self.workspace_dir / ".orchestrator" / "api_stats.json"
        self.load_stats()
    
    async def check_rate_limit(self, provider: str) -> bool:
        """Check if we're within rate limits"""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        if provider not in self.request_history:
            return True
        
        # Clean old requests
        self.request_history[provider] = [
            req_time for req_time in self.request_history[provider]
            if req_time > one_minute_ago
        ]
        
        # Check if we exceeded limit
        limit = self.rate_limits.get(provider, {}).get("calls_per_minute", 60)
        if len(self.request_history[provider]) >= limit:
            wait_time = self._calculate_wait_time(provider)
            print(f"⚠️  Rate limit approaching for {provider}")
            print(f"   Current requests: {len(self.request_history[provider])}/{limit}")
            print(f"   Consider waiting {wait_time:.1f} seconds before next call")
            return False
        
        return True
    
    def log_request(self, provider: str, tokens_used: int = 0, success: bool = True):
        """Log API request for tracking"""
        self.request_history[provider].append(datetime.now())
        
        if success:
            self.stats_file.parent.mkdir(parents=True, exist_ok=True)
            self._update_stats(provider, tokens_used)
    
    def _calculate_wait_time(self, provider: str) -> float:
        """Calculate recommended wait time before next request"""
        if not self.request_history[provider]:
            return 0
        
        oldest_request = self.request_history[provider][0]
        current_time = datetime.now()
        elapsed = (current_time - oldest_request).total_seconds()
        wait_time = max(0, 60 - elapsed)  # Wait until oldest request is 1 minute old
        
        return wait_time
    
    async def wait_if_needed(self, provider: str):
        """Wait if rate limit is about to be exceeded"""
        while not await self.check_rate_limit(provider):
            wait_time = self._calculate_wait_time(provider)
            if wait_time > 0:
                print(f"⏳ Waiting {wait_time:.1f}s to respect rate limits...")
                await asyncio.sleep(min(wait_time, 10))  # Max 10s wait
    
    def get_stats(self) -> Dict:
        """Get current API usage statistics"""
        return {
            "timestamp": datetime.now().isoformat(),
            "request_history": {
                provider: len(requests) for provider, requests in self.request_history.items()
            },
            "estimated_cost": self._calculate_estimated_cost()
        }
    
    def _calculate_estimated_cost(self) -> Dict[str, float]:
        """Calculate estimated costs (should be $0 for free models)"""
        costs = {}
        for provider, cost_config in self.cost_tracking.items():
            requests = len(self.request_history.get(provider, []))
            # Assuming average 1000 tokens per request
            estimated_tokens = requests * 1000
            estimated_cost = (estimated_tokens / 1000) * cost_config.get("cost_per_1k_tokens", 0)
            costs[provider] = estimated_cost
        
        return costs
    
    def _update_stats(self, provider: str, tokens_used: int):
        """Update statistics file"""
        try:
            stats = {}
            if self.stats_file.exists():
                with open(self.stats_file, 'r') as f:
                    stats = json.load(f)
            
            if provider not in stats:
                stats[provider] = {"requests": 0, "tokens": 0}
            
            stats[provider]["requests"] += 1
            stats[provider]["tokens"] += tokens_used
            stats[provider]["last_updated"] = datetime.now().isoformat()
            
            with open(self.stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not update stats: {e}")
    
    def load_stats(self):
        """Load previous statistics if available"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    stats = json.load(f)
                    print(f"📊 Loaded API usage statistics:")
                    for provider, data in stats.items():
                        print(f"   {provider}: {data.get('requests', 0)} requests, {data.get('tokens', 0)} tokens")
            except Exception as e:
                print(f"⚠️  Could not load stats: {e}")
    
    def print_summary(self):
        """Print usage summary"""
        stats = self.get_stats()
        print(f"\n📊 API USAGE SUMMARY")
        print(f"{'='*50}")
        print(f"Timestamp: {stats['timestamp']}")
        print(f"Recent Requests (last minute):")
        for provider, count in stats['request_history'].items():
            print(f"  {provider}: {count} requests")
        print(f"Estimated Costs:")
        for provider, cost in stats['estimated_cost'].items():
            print(f"  {provider}: ${cost:.4f}")
        print(f"{'='*50}\n")


class ConcurrencyManager:
    """Manages concurrent API requests with proper throttling"""
    
    def __init__(self, max_concurrent_requests: int = 10):
        self.max_concurrent = max_concurrent_requests
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.active_requests = 0
    
    async def execute(self, coro, provider: str, rate_limiter: RateLimiter):
        """Execute coroutine with rate limiting and concurrency control"""
        await rate_limiter.wait_if_needed(provider)
        
        async with self.semaphore:
            self.active_requests += 1
            try:
                result = await coro
                rate_limiter.log_request(provider)
                return result
            finally:
                self.active_requests -= 1