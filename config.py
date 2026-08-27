import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Model Selection ---
# Set to True to use Groq API (needs GROQ_API_KEY in .env), False to use local Ollama
USE_GROQ = True

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
COLLECTION_NAME = "tickets"

# --- Agentic Layer Thresholds ---
CONFIDENCE_THRESHOLD = 0.75          # Above this → fast centroid path (no LLM)
MEDIUM_CONFIDENCE_THRESHOLD = 0.40   # Below this → direct escalation (no LLM)
                                     # Between 0.40–0.75 → LLM judge re-classifies
NOVELTY_SIMILARITY_THRESHOLD = 0.20  # If best-match similarity < this → NOVEL_TICKET
REPEAT_THRESHOLD = 3        # Number of similar tickets to trigger automation suggestion
REPEAT_WINDOW_DAYS = 7      # Time window for repeat detection
SIMILARITY_THRESHOLD = 0.85 # Cosine similarity score to consider tickets "similar"

# --- Categories & Routing ---
CATEGORIES = [
    "Infrastructure", 
    "Application", 
    "Security",
    "Database", 
    "Network", 
    "Access Management"
]

ROUTING = {
    "Infrastructure": "Cloud Platform Engineering",
    "Application": "Application Support Team",
    "Security": "Security Operations Center (SOC)",
    "Database": "Database Administration (DBA)",
    "Network": "Network Operations Center (NOC)",
    "Access Management": "Identity & Access Management (IAM)",
    "Unknown": "General Support L1"
}
