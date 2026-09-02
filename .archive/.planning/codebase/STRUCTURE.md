# Structure

## Directory Layout

```
/home/devesh/Hackathon/
├── app.py                              # Streamlit UI (main entry point, 499 lines)
├── config.py                           # All constants, thresholds, model config (50 lines)
├── requirements.txt                    # Python dependencies (12 lines, no version pins)
├── implementation_plan.md              # Hackathon engineering roadmap (632 lines)
├── tillnow.md                          # Progress tracker (48 lines)
├── .gitignore                          # Standard Python + project-specific ignores
│
├── core/                               # Core business logic
│   ├── __init__.py                     # Empty init
│   ├── embeddings.py                   # Shared embedding model + ChromaDB client (82 lines)
│   ├── classifier.py                   # Ticket classification engine (191 lines)
│   ├── rag.py                          # RAG resolution engine (129 lines)
│   └── agent.py                        # Agentic escalation/automation layer (115 lines)
│
├── data/                               # Data generation and storage
│   ├── __init__.py                     # Empty init
│   ├── generate_data.py                # Main generator: 2×500 tickets via Ollama (214 lines)
│   ├── generate_100.py                 # Smaller batch generator (100 tickets)
│   ├── generate_100_batch2.py          # Second small batch generator
│   └── synthetic_tickets_merged.csv    # Generated dataset (150 tickets)
│
├── evaluation/                         # Evaluation framework (stub)
│   └── __init__.py                     # Empty init (no evaluate.py or llm_judge.py yet)
│
├── chroma_db/                          # ChromaDB persistent storage
│   ├── chroma.sqlite3                  # SQLite database (520KB)
│   └── 33b296e0-.../                   # HNSW index segment
│
├── venv/                               # Python virtual environment
│
├── .agents/                            # Agent rules (phase.md, progress.md, workspace.md, ollama.md)
│   └── rules/
│
├── Next-Generation AI Ticket...v1.md   # Architecture spec document v1 (28KB)
└── Next-Generation AI Ticket...v2.md   # Architecture spec document v2 (25KB)
```

## Key Locations

| What | Where |
|------|-------|
| Application entry point | `app.py` |
| Configuration | `config.py` |
| Embedding & DB singletons | `core/embeddings.py` |
| Classification logic | `core/classifier.py` |
| RAG resolution pipeline | `core/rag.py` |
| Agent escalation/automation | `core/agent.py` |
| Training data | `data/synthetic_tickets_merged.csv` |
| Data generation scripts | `data/generate_data.py` |
| Vector database | `chroma_db/` |
| Progress tracking | `tillnow.md` |
| Implementation blueprint | `implementation_plan.md` |

## Naming Conventions

- **Files:** `snake_case.py` throughout
- **Classes:** `PascalCase` — `TicketClassifier`, `ResolutionEngine`, `AgenticLayer`
- **Methods:** `snake_case` — `classify()`, `suggest_resolution()`, `_detect_repeats()`
- **Private methods:** Prefixed with `_` — `_build_centroids()`, `_cosine_similarity()`, `_generate_ollama()`
- **Constants:** `UPPER_SNAKE_CASE` in `config.py` — `CONFIDENCE_THRESHOLD`, `OLLAMA_MODEL`
- **Module globals:** Prefixed with `_` for singletons — `_model`, `_client`, `_collection`
