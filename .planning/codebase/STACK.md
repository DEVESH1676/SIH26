# Stack

## Languages & Runtime

| Language | Version | Usage |
|----------|---------|-------|
| Python | 3.14 | All backend logic, data generation, UI |

## Frameworks & Libraries

### Core Application

| Library | Purpose | Notes |
|---------|---------|-------|
| `streamlit` | Web UI dashboard | Single-file app at `app.py`, 3-tab layout |
| `langchain` | Orchestration framework | Used for prompt templates, chain composition |
| `langchain-community` | Community integrations | Ollama/Groq adapters |
| `langchain-groq` | Groq API binding | Cloud LLM alternative |
| `chromadb` | Vector database | Persistent local storage at `./chroma_db/`, SQLite backend |
| `sentence-transformers` | Embedding model | `all-MiniLM-L6-v2`, 384-dim vectors, CPU-compatible |
| `groq` | Groq SDK | Direct API access for cloud inference |

### Data & Visualization

| Library | Purpose | Notes |
|---------|---------|-------|
| `scikit-learn` | ML metrics | `cosine_similarity`, `classification_report`, `f1_score` |
| `pandas` | Data manipulation | CSV reading, DataFrame ops |
| `plotly` | Interactive charts | Pie charts, bar charts, horizontal bars in Streamlit |
| `python-dotenv` | Environment config | Loads `.env` for API keys |
| `numpy` | Array operations | Centroid computation, embedding math |
| `requests` | HTTP client | Direct Ollama REST API calls (bypasses LangChain) |

## Configuration

- **Config file:** `config.py` — all constants, thresholds, model names, API keys
- **Environment:** `.env` file for `GROQ_API_KEY` (loaded via `python-dotenv`)
- **Virtual environment:** `venv/` directory (Python 3.14)

## LLM Backend

| Provider | Model | Usage |
|----------|-------|-------|
| **Ollama** (primary) | `qwen2.5-gpu:latest` | Resolution generation via RAG |
| **Groq** (alternative) | `llama3-70b-8192` | Cloud fallback, toggled via `USE_GROQ` in `config.py` |

- Ollama endpoint: `http://192.168.137.1:11434` (remote host, not localhost)
- RAG module uses direct REST calls to Ollama (`/api/chat`) — **LangChain is NOT used for LLM calls** due to timeout/hanging issues discovered during development

## Embedding Model

- **Model:** `all-MiniLM-L6-v2` via `sentence-transformers`
- **Dimensions:** 384
- **Similarity metric:** Cosine similarity (configured in ChromaDB via `hnsw:space: cosine`)

## Package Management

- `requirements.txt` — flat dependency list, no version pins
- No `setup.py`, `pyproject.toml`, or `poetry.lock`
