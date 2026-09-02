# Concerns

## Technical Debt

### 1. `sys.path.append` Hack — Every Core Module

**Files:** `core/classifier.py`, `core/rag.py`, `core/agent.py`, `core/embeddings.py`, `data/generate_data.py`

```python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
```

Every module manually manipulates `sys.path` to import `config`. This is fragile and breaks if the project is installed as a package or run from unexpected working directories. Should be replaced with proper Python packaging (`pyproject.toml`, relative imports, or `-m` module execution).

### 2. No Version Pinning in `requirements.txt`

All dependencies listed without versions. Builds are non-reproducible — a future `pip install` could pull breaking changes.

### 3. CSV Filename Mismatch

- `app.py` loads `data/synthetic_tickets.csv` (line 168)
- The actual file is `data/synthetic_tickets_merged.csv`
- This means the Analytics tab shows "Database empty" unless the file is renamed

### 4. Hardcoded Ollama Host

`config.py` sets `OLLAMA_BASE_URL = "http://192.168.137.1:11434"` — a specific LAN IP. Will break on any other network.

### 5. No Data Persistence for Session History

`st.session_state.history` stores ticket analysis results in memory only. Lost on every Streamlit restart/rerun.

## Security Concerns

### 1. `GROQ_API_KEY` in Config

`config.py` loads API key from `.env` with empty string fallback — safe. The `.env` file is in `.gitignore` — **good practice**. However, `config.py` exposes the key as a module-level variable (`GROQ_API_KEY`) accessible from any importing module.

### 2. `unsafe_allow_html=True` in Streamlit

`app.py` uses `st.markdown(..., unsafe_allow_html=True)` extensively for custom HTML rendering. While this is standard for Streamlit styling, it opens potential XSS vectors if user input is rendered without sanitization. Currently, user-submitted ticket text is NOT directly rendered in HTML templates — ticket details go through the ML pipeline, not raw HTML.

### 3. No Input Validation

Ticket title and description are passed directly to embedding model and Ollama prompts. No sanitization, length limits, or prompt injection protection.

## Performance Concerns

### 1. Centroid Computation on Every Cold Start

`TicketClassifier.__init__()` calls `self.collection.get(include=["embeddings", "metadatas"])` to load ALL embeddings from ChromaDB, then computes centroids. With 150 tickets this is fast, but would degrade significantly at 10K+ tickets.

### 2. Three Separate Embedding Calls per Ticket

When submitting a ticket with RAG enabled, the embedding model encodes the same text 3 times:
- Once in `classifier.classify()` 
- Once in `agent._detect_repeats()`
- Once in `rag.suggest_resolution()`

These could share a single embedding computation.

### 3. Ollama Cold Start Latency

The Ollama model on the remote host may need to load into GPU memory on first call, causing multi-second delays.

## Fragile Areas

### 1. ChromaDB Collection Coupling

All modules assume a single collection named `"tickets"` exists and is populated. If ChromaDB is empty or the collection is missing, `classifier.py` prints a warning but continues with empty centroids — classification would return meaningless results.

### 2. RAG Quality Depends on Data Volume

With only 150 tickets, the RAG retrieval may return poor matches for uncommon issues. The system has no mechanism to indicate "no good match found."

### 3. Agent Repeat Detection Without Time Filtering

`core/agent.py` queries ChromaDB for repeats but does NOT filter by `created_at` date (the `_detect_repeats` method doesn't use any date filtering, unlike the implementation_plan.md specification). All historical tickets are considered "recent."

## Missing Features (from Implementation Plan)

| Feature | Status | Location |
|---------|--------|----------|
| LLM zero-shot fallback classifier | ❌ Not implemented | Was planned for `core/classifier.py` |
| Evaluation suite (F1, accuracy, confusion matrix) | ❌ Not implemented | `evaluation/` is empty |
| LLM-as-judge evaluation | ❌ Not implemented | `evaluation/` is empty |
| Settings tab in UI | ❌ Not implemented | `app.py` only has 3 tabs |
| `created_at` date filtering in agent repeat detection | ❌ Not implemented | `core/agent.py` |
| README.md | ❌ Not created | Project root |
