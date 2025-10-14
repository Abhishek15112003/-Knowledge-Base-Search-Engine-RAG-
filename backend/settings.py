from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Knowledge RAG API"
    app_env: str = "dev"
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        
settings = Settings()