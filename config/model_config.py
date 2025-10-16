
import os
from crewai import LLM

class ModelConfig:
    def __init__(self):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")

        if not self.openrouter_key or not self.groq_key:
            raise ValueError("❌ API keys not found! Check your .env file")

    def get_model_for_role(self, role: str) -> LLM:
        """Get optimal free model for specific agent role with proper reasoning configuration"""

        model_assignments = {
            # Strategic roles - use DeepSeek models with effort-based reasoning
            "master_orchestrator": self._create_reasoning_llm(
                "deepseek/deepseek-chat-v3.1:free", 0.1, reasoning_config={"effort": "medium"}
            ),
            "project_manager": self._create_reasoning_llm(
                "deepseek/deepseek-chat-v3.1:free", 0.2, reasoning_config={"effort": "high"}
            ),

            # Development roles - mixed approach
            "system_architect": self._create_reasoning_llm(
                "deepseek/deepseek-chat-v3.1:free", 0.1, reasoning_config={"effort": "high"}
            ),
            "senior_developer": self._create_reasoning_llm(
                "nvidia/nemotron-nano-9b-v2:free", 0.2, reasoning_config={"effort": "medium"}
            ),

            # Qwen models - use max_tokens approach (some support thinking_budget)
            "backend_developer": self._create_reasoning_llm(
                "qwen/qwen3-coder:free", 0.2, reasoning_config={"max_tokens": 1000}
            ),
            "frontend_developer": self._create_reasoning_llm(
                "qwen/qwen3-coder:free", 0.3, reasoning_config={"max_tokens": 1000}
            ),

            # Support roles
            "qa_engineer": self._create_reasoning_llm(
                "deepseek/deepseek-chat-v3.1:free", 0.2, reasoning_config={"effort": "low"}
            ),
            "devops_engineer": self._create_reasoning_llm(
                "qwen/qwen3-coder:free", 0.2, reasoning_config={"max_tokens": 800}
            ),
            "documentation_writer": self._create_reasoning_llm(
                "x-ai/grok-4-fast:free", 0.4, reasoning_config={"effort": "low"}
            )
        }

        return model_assignments.get(
            role, 
            self._create_reasoning_llm("x-ai/grok-4-fast:free", 0.3, reasoning_config={"effort": "medium"})
        )

    def _create_reasoning_llm(self, model: str, temperature: float, reasoning_config: dict) -> LLM:
        """Create OpenRouter LLM with proper reasoning configuration"""
        return LLM(
            model=f"openrouter/{model}",
            api_key=self.openrouter_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
            max_tokens=4000,
            reasoning=reasoning_config  # Direct reasoning parameter - not in extra_body!
        )

    def _create_groq_reasoning_llm(self, model: str, temperature: float, reasoning_config: dict) -> LLM:
        """Create Groq LLM with reasoning - for Grok models"""
        return LLM(
            model=f"groq/{model}",
            api_key=self.groq_key,
            temperature=temperature,
            max_tokens=4000,
            reasoning=reasoning_config  # Direct reasoning parameter
        )

    def _create_openrouter_llm(self, model: str, temperature: float) -> LLM:
        """Create regular OpenRouter LLM without reasoning"""
        return LLM(
            model=f"openrouter/{model}",
            api_key=self.openrouter_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
            max_tokens=4000,
            timeout=120
        )
