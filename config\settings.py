import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o")
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "10"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
