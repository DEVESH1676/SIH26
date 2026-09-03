from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "MoSPI AI Learning Platform"
    app_env: str = "development"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    sqlite_path: str = "data/mospi_learning.db"
    chroma_persist_dir: str = "data/chroma"
    chroma_collection: str = "mospi_embeddings"
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"
    groq_embed_model: str = "all-MiniLM-L6-v2"
    ollama_base_url: Optional[str] = None
    ollama_model: str = "llama3.3"
    ollama_embed_model: str = "nomic-embed-text"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expiry_minutes: int = 60
    jwt_refresh_token_expiry_days: int = 7
    igot_api_base_url: str = "https://api.igotindia.gov.in/v1"
    igot_api_key: Optional[str] = None
    igot_cache_ttl_seconds: int = 10800
    igot_courses_per_request: int = 20
    nssta_base_url: Optional[str] = None
    nssta_api_key: Optional[str] = None
    rate_limit_per_minute: int = 60
    cors_origins: list[str] = ["http://localhost:5173"]
    max_document_chars: int = 50000
    max_upload_size_mb: int = 100
    upload_dir: str = "data/uploads"
    log_level: str = "INFO"
    log_format: str = "json"
    default_quiz_questions: int = 10

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

def get_settings() -> Settings:
    return Settings()
