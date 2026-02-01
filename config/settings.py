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
        
        # Paths
        self.prompts_dir = Path(__file__).parent.parent / "prompts"
        
    def get_llm(self, provider="openai"):
        """Get LLM instance based on provider"""
        if provider == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                api_key=self.openai_api_key
            )
        elif provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model="claude-3-sonnet-20240229",
                temperature=self.temperature,
                api_key=self.anthropic_api_key
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")

settings = Settings()
