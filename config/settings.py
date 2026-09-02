from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """MoSPI AI Learning Platform settings — loaded from .env with defaults."""

    # ── LLM Configurations ──────────────────────────────────
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    use_groq: bool = True

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-gpu:latest"

    # ── Embedding Configurations ────────────────────────────
    embedding_model_name: str = "all-MiniLM-L6-v2"
    chroma_db_path: str = "./chroma_db"
    collection_name: str = "courses"          # Changed from "tickets"
    
    # ── iGOT Karmayogi Integration ─────────────────────────
    igot_api_base_url: str = "https://api.igot-karmayogi.gov.in/api/v1"
    igot_api_key: str = ""
    igot_cache_ttl_seconds: int = 3600        # Cache catalog for 1 hour
    igot_courses_per_request: int = 50

    # ── Assessment & Quiz ──────────────────────────────────
    max_document_chars: int = 25000            # Increased from 5000
    max_quiz_questions: int = 20               # Increased from 10
    default_quiz_questions: int = 5
    quiz_difficulty_levels: List[str] = ["beginner", "intermediate", "advanced"]

    # ── File Upload ─────────────────────────────────────────
    max_upload_size_mb: int = 50
    allowed_file_types: List[str] = [
        "pdf", "docx", "pptx", "txt", "mp4", "mp3", "wav"
    ]

    # ── Authentication ──────────────────────────────────────
    jwt_secret_key: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expiry_minutes: int = 60
    jwt_refresh_token_expiry_days: int = 7

    # ── Database ────────────────────────────────────────────
    sqlite_path: str = "./data/learning.db"

    # ── Competency Framework ────────────────────────────────
    confidence_threshold: float = 0.75
    medium_confidence_threshold: float = 0.40
    novelty_similarity_threshold: float = 0.20

    # ── Security ────────────────────────────────────────────
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    rate_limit_per_minute: int = 60
    max_login_attempts: int = 5
    password_min_length: int = 8

    # ── Multi-language ──────────────────────────────────────
    supported_languages: List[str] = [
        "en", "hi", "bn", "te", "ta", "mr", "gu", "ur",
        "pa", "ml", "or", "as", "ks", "ne", "sd"
    ]
    default_language: str = "en"

    # ── Logging ─────────────────────────────────────────────
    log_level: str = "INFO"
    log_format: str = "json"  # or "text"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
