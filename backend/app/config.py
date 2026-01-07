from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    flight_api_key: str = os.getenv("FLIGHT_API_KEY", "")
    flight_api_url: str = os.getenv("FLIGHT_API_URL", "https://api.example.com/flights")
    
    # LLM Configuration
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
    
    # Server Configuration
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()