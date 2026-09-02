# Conventions

## Code Style

- **Python style:** Generally PEP 8 compliant
- **Indentation:** 4 spaces
- **Quotes:** Double quotes for strings throughout
- **Line length:** No strict limit enforced; some lines in `app.py` exceed 120 chars (CSS/HTML blocks)
- **Imports:** Grouped into stdlib → third-party → local, but with `sys.path.append` hacks rather than proper packaging

## Module Pattern

Every core module follows the same pattern:

```python
"""
Module docstring describing purpose.
"""
import os
import sys

# Hack to allow absolute imports from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.embeddings import get_embedding_model, get_chroma_collection

class MainClass:
    def __init__(self):
        self.model = get_embedding_model()
        self.collection = get_chroma_collection()
    
    def public_method(self, ...):
        ...
    
    def _private_helper(self, ...):
        ...

# --- CLI Test ---
if __name__ == "__main__":
    # Inline test code
```

Key characteristics:
- **`sys.path.append` hack** in every module for cross-directory imports
- **Singleton pattern** via `embeddings.py` globals — all modules share one model/collection instance
- **CLI test blocks** at bottom of every module for standalone testing
- **Docstrings** on classes and key methods (not on all helpers)

## Error Handling

- **Minimal error handling** overall — try/except only in `rag.py` for Ollama HTTP calls
- **No logging framework** — uses `print()` statements throughout
- **ChromaDB failures** would crash the app (no graceful degradation)
- **Ollama timeout** returns error string instead of raising (returns `"Error connecting to Ollama: ..."`)

## Configuration Pattern

- All configuration in `config.py` as module-level constants
- `.env` loaded via `python-dotenv` at import time
- Streamlit sidebar allows runtime override of thresholds (`confidence_threshold`, `similarity_threshold`)
- RAG toggle is a UI switch (`generate_resolution`), not a config value

## Data Patterns

- **CSV as source of truth** for ticket data
- **Vector DB (ChromaDB) as derived store** — rebuilt from CSV via `embeddings.py`
- **No database migrations** — ChromaDB is treated as disposable/rebuildable
- **Session state** (`st.session_state.history`) for in-memory ticket history, lost on restart

## Dependency Injection

- No DI framework — dependencies are resolved in constructors via `embeddings.py` singletons
- `config.py` acts as a global configuration registry
- Tight coupling: all core modules import `config` and `core.embeddings` directly
