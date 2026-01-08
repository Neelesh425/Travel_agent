from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Ollama settings
    ollama_model: str = "llama3.2:latest"
    ollama_host: str = "http://localhost:11434"
    
    # API settings
    flight_api_key: str = ""
    flight_api_url: str = ""
    
    # Server settings
    frontend_url: str = "http://localhost:5173"
    backend_port: int = 8000
    
    # Database settings
    database_url: str = "sqlite:///./travel_booking.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()