import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Model Selection ---
# Set to True to use Groq API (needs GROQ_API_KEY in .env), False to use local Ollama
USE_GROQ = os.getenv("USE_GROQ", "True").lower() == "true"

# --- LLM Configurations ---
# Groq specific
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Fallback to Streamlit secrets if deployed on Streamlit Community Cloud
if not GROQ_API_KEY:
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

GROQ_MODEL = "llama-3.3-70b-versatile"

# Ollama specific
OLLAMA_MODEL = "qwen2.5-gpu:latest" 
OLLAMA_BASE_URL = "http://192.168.137.1:11434"

# --- Embedding Configurations ---
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
CHROMA_DB_DIR = "./chroma_db"
COLLECTION_NAME = "courses"

# --- LMS Agentic Layer Thresholds ---
CONFIDENCE_THRESHOLD = 0.75          # Above this → high confidence skill gap match
MEDIUM_CONFIDENCE_THRESHOLD = 0.40   # Below this → manual assessment required
                                     # Between 0.40–0.75 → LLM re-evaluates
NOVELTY_SIMILARITY_THRESHOLD = 0.20  # If best-match similarity < this → NOVEL_SKILL
REPEAT_THRESHOLD = 3        # Number of failed quiz attempts to trigger mentor suggestion
REPEAT_WINDOW_DAYS = 7      # Time window for attempt detection
SIMILARITY_THRESHOLD = 0.85 # Cosine similarity score to consider courses "similar"

# --- MoSPI FRAC Competency Domains ---
CATEGORIES = [
    "Statistical Competencies", 
    "Functional & Digital Competencies", 
    "Behavioral Competencies"
]

ROUTING = {
    "Statistical Competencies": "NSSTA Advanced Training",
    "Functional & Digital Competencies": "iGOT Karmayogi Online Platform",
    "Behavioral Competencies": "iGOT Karmayogi Ethics Modules",
}

# --- iGOT Karmayogi API Configurations ---
IGOT_API_BASE_URL = os.getenv("IGOT_API_BASE_URL", "https://karmayogi.nic.in/api")
IGOT_API_KEY = os.getenv("IGOT_API_KEY", "")

# --- Compliance & Settings (SSIP/MeitY) ---
DATA_LOCALITY_STRICT = os.getenv("DATA_LOCALITY_STRICT", "True").lower() == "true"
LOG_RETENTION_DAYS = int(os.getenv("LOG_RETENTION_DAYS", "90"))

# --- Multi-Language Settings ---
SUPPORTED_LANGUAGES = ["en", "hi", "bn", "te", "mr", "ta", "ur", "gu"]
DEFAULT_LANGUAGE = "en"

# --- File Processing & Upload Limits ---
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
SUPPORTED_FILE_FORMATS = [".pdf", ".docx", ".pptx", ".mp4", ".mp3"]
CHUNK_SIZE_TEXT = int(os.getenv("CHUNK_SIZE_TEXT", "2000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
