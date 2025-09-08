from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    CORS_ORIGINS: List[str] = eval(os.getenv("CORS_ORIGINS", '["http://localhost:5173", "http://localhost:3000"]'))
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    
    DATAFORSEO_LOGIN: str = os.getenv("DATAFORSEO_LOGIN", "")
    DATAFORSEO_PASSWORD: str = os.getenv("DATAFORSEO_PASSWORD", "")
    
    class Config:
        env_file = os.getenv("ENV_FILE_NAME", ".env.local")

settings = Settings()
