from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5-nano"
    OPENAI_TEMPERATURE: float = 1.0
    OPENAI_MAX_TOKENS: int = 10000
    
    DATAFORSEO_LOGIN: str = ""
    DATAFORSEO_PASSWORD: str = ""
    
    model_config = {
        "env_file": ".env.local",
    }

settings = Settings()
