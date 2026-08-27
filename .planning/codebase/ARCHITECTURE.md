# Architecture

## Pattern

**Monolithic single-process application** with a layered internal architecture.

The system follows a **pipeline pattern**: incoming ticket → classification → agent reasoning → optional RAG resolution → UI presentation.

```
┌─────────────────────────────────────────────────────┐
│                   Streamlit UI (app.py)              │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ Submit   │  │  Analytics   │  │  Agent Log    │  │
│  │ Ticket   │  │  Dashboard   │  │  (History)    │  │
│  └────┬─────┘  └──────┬───────┘  └───────────────┘  │
│       │               │                              │
├───────┼───────────────┼──────────────────────────────┤
│       ▼               ▼                              │
│  ┌─────────────────────────────────────────────┐     │
│  │          Core Logic Layer (core/)            │     │
│  │                                              │     │
│  │  classifier.py ──→ agent.py ──→ rag.py      │     │
│  │       │                │            │        │     │
│  │       └────────────────┴────────────┘        │     │
│  │                    │                          │     │
│  │              embeddings.py                   │     │
│  └──────────────────┬───────────────────────────┘     │
│                     │                                 │
│              ┌──────▼──────┐                          │
│              │  ChromaDB   │                          │
│              │ (chroma_db/)│                          │
│              └──────┬──────┘                          │
│                     │                                 │
│              ┌──────▼──────┐                          │
│              │  Ollama API │                          │
│              │  (remote)   │                          │
│              └─────────────┘                          │
└─────────────────────────────────────────────────────┘
```

## Layers

### 1. Presentation Layer — `app.py`

- Streamlit dashboard with 3 tabs: Submit Ticket, Analytics, Agent Log
- Custom CSS: glassmorphism, dark theme (#0f172a), gradient animations
- Session state for ticket history (in-memory, not persisted)
- Cached model loading via `@st.cache_resource`

### 2. Core Logic Layer — `core/`

- **`classifier.py` (TicketClassifier):** Embedding-based classification using dual approach:
  1. Centroid similarity (primary): computes mean embedding per category, classifies via cosine similarity
  2. Direct search similarity (validation): top-5 nearest neighbor search for confidence adjustment
  - Confidence = weighted blend: 60% centroid score + 40% search agreement
  - Falls back to search-based classification when confidence < threshold

- **`agent.py` (AgenticLayer):** Decision engine for:
  1. Escalation: flags tickets below confidence threshold for human review
  2. Repeat detection: identifies recurring patterns (≥3 similar tickets above 0.85 similarity)

- **`rag.py` (ResolutionEngine):** RAG pipeline:
  1. Retrieves top-3 similar tickets from ChromaDB
  2. Constructs prompt with past resolutions as context
  3. Calls Ollama REST API directly for resolution generation

### 3. Data Layer — `core/embeddings.py`

- Singleton pattern for `SentenceTransformer` model and `ChromaDB` client
- `ingest_tickets()`: CSV → embeddings → ChromaDB upsert
- Shared by all core modules via `get_embedding_model()` and `get_chroma_collection()`

## Data Flow

```
User Input (title + description)
    │
    ▼
[Embed] → SentenceTransformer('all-MiniLM-L6-v2') → 384-dim vector
    │
    ├──→ [Classify] → centroid similarity + search validation → category + confidence
    │         │
    │         ▼
    ├──→ [Agent] → escalation check + repeat detection → agent actions
    │
    └──→ [RAG] (optional, user toggle) → retrieve similar → Ollama generate → resolution
    │
    ▼
[UI] → render classification, agent actions, resolution, similar tickets
```

## Entry Points

- `streamlit run app.py` — main application
- `python core/embeddings.py` — ingest CSV data into ChromaDB
- `python core/classifier.py` — CLI test of classifier
- `python core/rag.py` — CLI test of RAG engine
- `python core/agent.py` — CLI test of agent layer
- `python data/generate_data.py` — generate synthetic ticket data

## Key Abstractions

- **TicketClassifier:** Self-contained; builds centroids on init, classifies via `classify(title, desc)`
- **ResolutionEngine:** Self-contained; retrieves + generates via `suggest_resolution(title, desc)`
- **AgenticLayer:** Self-contained; orchestrates via `process(title, desc, classification_result)`
- **Embeddings module:** Provides singletons for shared resources (model, collection)
