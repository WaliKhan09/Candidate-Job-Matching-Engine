import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # This is the name of our app
    APP_NAME: str = "Semantic Matching Engine"
    
    # We are using a small, fast model from HuggingFace
    # It turns text into a list of numbers (embeddings)
    MODEL_NAME: str = "all-MiniLM-L6-v2"
    
    # This is where our SQL database will be saved on your computer
    DB_URL: str = "sqlite:///./matching_engine.db"
    
    # How many top candidates do we want to see?
    TOP_K: int = 5

    # This part allows us to overwrite these settings with an .env file
    class Config:
        env_file = ".env"

# Create a single 'settings' object that the rest of the app can use
settings = Settings()
