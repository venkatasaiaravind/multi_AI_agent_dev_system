import os
from crewai import LLM

class ModelConfig:
    """Manages LLM model selection and configuration for all agent roles"""

    def __init__(self):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")

        if not self.openrouter_key:
            raise ValueError("❌ OPENROUTER_API_KEY not found! Check your .env file")

    def get_model_for_role(self, role: str) -> LLM:
        """Get optimal free model for specific agent role"""
        model_assignments = {
            "system_architect": self._create_openrouter_llm(
                "deepseek/deepseek-chat-v3.1:free",
                temperature=0.1,
                thinking_budget=4000
            ),
            "backend_developer": self._create_openrouter_llm(
                "qwen/qwen3-coder:free",
                temperature=0.2
            ),
            "frontend_developer": self._create_openrouter_llm(
                "qwen/qwen3-coder:free",
                temperature=0.3
            ),
            "data_scientist": self._create_openrouter_llm(
                "qwen/qwen3-coder:free",
                temperature=0.2
            ),
            "devops_engineer": self._create_openrouter_llm(
                "qwen/qwen3-coder:free",
                temperature=0.2
            ),
        }
        return model_assignments.get(
            role,
            self._create_openrouter_llm("google/gemini-2.0-flash-exp:free", temperature=0.3)
        )

    def _create_openrouter_llm(self, model: str, temperature: float, thinking_budget: int = None) -> LLM:
        """Create OpenRouter LLM"""
        llm_config = {
            "model": f"openrouter/{model}",
            "api_key": self.openrouter_key,
            "base_url": "https://openrouter.ai/api/v1",
            "temperature": temperature,
            "max_tokens": 8000,
            "timeout": 180
        }
        if thinking_budget:
            llm_config["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget
            }
        return LLM(**llm_config)
