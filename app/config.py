import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Semantic Matching Engine"
    
    MODEL_NAME: str = "all-MiniLM-L6-v2"
    
    DB_URL: str = "sqlite:///./matching_engine.db"
    
    TOP_K: int = 5

    class Config:
        env_file = ".env"

settings = Settings()
