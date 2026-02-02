import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Try to load from Streamlit secrets (for cloud deployment)
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        for key in ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'MODEL_NAME', 'TEMPERATURE']:
            if key in st.secrets:
                os.environ[key] = str(st.secrets[key])
except Exception:
    pass  # Not running in Streamlit or secrets not configured

class Settings:
    """Configuration settings for the LangGraph system"""
    
    def __init__(self):
        # API Keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        # Model settings
        self.model_name = os.getenv("MODEL_NAME", "gpt-4")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        
        # Agent settings
        self.max_iterations = 5
        self.min_iterations = 2
        
        # Agent-specific model settings (có thể override)
        self.agent_models = {
            "input_normalizer": os.getenv("INPUT_NORMALIZER_MODEL", "gpt-4o-mini"),
            "proposer": os.getenv("PROPOSER_MODEL", "gpt-4o-mini"),
            "critic": os.getenv("CRITIC_MODEL", "gpt-4o"),
            "challenger": os.getenv("CHALLENGER_MODEL", "gpt-4o"),  # Changed from Claude to GPT-4o
            "synthesizer": os.getenv("SYNTHESIZER_MODEL", "gpt-4o"),
        }
        
        # Paths
        self.prompts_dir = Path(__file__).parent.parent / "prompts"
        
    def get_llm(self, provider="openai", model_override=None):
        """Get LLM instance based on provider and model"""
        # Auto-detect provider from model name
        if model_override and "claude" in model_override.lower():
            provider = "anthropic"
        
        if provider == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=model_override or self.model_name,
                temperature=self.temperature,
                api_key=self.openai_api_key
            )
        elif provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            # Validate API key
            if not self.anthropic_api_key:
                raise ValueError("Anthropic API key not configured. Please add ANTHROPIC_API_KEY to .env")
            return ChatAnthropic(
                model=model_override or "claude-3-5-sonnet-20241022",
                temperature=self.temperature,
                api_key=self.anthropic_api_key
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def get_agent_llm(self, agent_name: str):
        """Get LLM for specific agent based on configuration"""
        model = self.agent_models.get(agent_name, self.model_name)
        
        # Auto-detect provider from model name
        if "claude" in model.lower():
            return self.get_llm("anthropic", model)
        else:
            return self.get_llm("openai", model)

settings = Settings()
