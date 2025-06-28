from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Cache settings
    CACHE_TTL: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"


settings = Settings()