# Phase 1: Backend Extraction (API Bridge) — Research

**Researched:** 2026-04-18
**Status:** Complete

---

## 1. Codebase Anatomy (What We're Wrapping)

### Core Modules — The Intelligence Brain

| Module | File | Key Classes/Functions | Return Type | Stateful? |
|--------|------|----------------------|-------------|-----------|
| Embeddings | `core/embeddings.py` (82 LOC) | `get_embedding_model()`, `get_chroma_collection()`, `ingest_tickets()` | SentenceTransformer, ChromaDB Collection | Yes — module-level singletons (`_model`, `_client`, `_collection`) |
| Classifier | `core/classifier.py` (349 LOC) | `TicketClassifier.classify()`, `TicketClassifier.find_repeats()` | dict with 11 fields | Yes — loads centroids on `__init__` |
| RAG Engine | `core/rag.py` (217 LOC) | `ResolutionEngine.suggest_resolution()`, `ResolutionEngine._rank_retrieved_chunks()` | dict with 3 fields | Yes — holds collection + embedding model |
| Agent Layer | `core/agent.py` (465 LOC) | `TriageAgent.run()`, `ResolutionAgent.run()`, `AutomationDiscoveryAgent.run()`, `AgenticLayer.process()` | dict per agent | TriageAgent: stateless. ResolutionAgent: stateless. AutoDiscovery: stateful (ChromaDB) |
| Judge | `core/judge.py` (191 LOC) | `ResolutionJudge.judge()` | dict with 8 fields | Stateless |
| Feedback | `core/feedback.py` (157 LOC) | `FeedbackStore.log_run()`, `FeedbackStore.get_all()` | list[dict] | Yes — SQLite connection |

### Configuration Layer

- `config.py` (63 LOC) — All thresholds, routing maps, model names, API keys
- `.env` — Contains `GROQ_API_KEY` only
- **Critical Pain Point:** `config.py` lines 16-22 have a Streamlit fallback for secrets (`import streamlit as st`). This must be removed/guarded for FastAPI context.

### sys.path Hack Problem

Every core module uses `sys.path.append(os.path.dirname(os.path.dirname(...)))` — a Streamlit-era hack. The new FastAPI `main.py` MUST be placed at project root alongside `config.py` so all `import config` and `from core.X import Y` statements resolve naturally. No module surgery needed if `main.py` sits at `/home/devesh/Hackathon/main.py`.

### The Monolith Pipeline (app.py — 1,405 LOC)

The critical function is `run_full_pipeline()` at line 771. Here's the exact execution chain that the API must replicate:

```
1. classify()         → TicketClassifier.classify(title, desc)
2. triage()           → TriageAgent.run(ticket, classification)
3. rag_retrieve()     → ResolutionEngine.suggest_resolution(title, desc)
4. rank_chunks()      → rag._rank_retrieved_chunks(raw_results)[:3]
5. resolve() [if enabled] → ResolutionAgent.run(ticket, ranked_chunks)
6. judge() [if enabled]   → ResolutionJudge.judge(ticket_dict, resolution_text)
7. automation_check() → AutomationDiscoveryAgent.run(resolved_ticket)
```

Steps 5-7 are conditional on the `generate_resolution` toggle (sidebar control in Streamlit).

---

## 2. FastAPI Architecture Decisions

### 2.1 Application Factory Pattern

Use FastAPI's `lifespan` context manager to load all ML models **once** at startup rather than per-request. This replicates Streamlit's `@st.cache_resource` behavior:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load all heavy resources
    app.state.classifier = TicketClassifier()
    app.state.rag_engine = ResolutionEngine()
    app.state.agents = {
        "triage": TriageAgent(),
        "resolution": ResolutionAgent(),
        "automation": AutomationDiscoveryAgent()
    }
    app.state.judge = ResolutionJudge()
    app.state.feedback = FeedbackStore()
    yield
    # Shutdown: cleanup
    app.state.feedback.close()

app = FastAPI(lifespan=lifespan, title="Nexus AI API", version="4.0")
```

**Why lifespan over startup events:** FastAPI deprecated `on_startup`/`on_shutdown` in favor of the lifespan pattern. It's the recommended approach for shared ML model loading.

### 2.2 SSE for Pipeline Streaming

FastAPI 0.135.0+ has **native SSE support** via `fastapi.sse.EventSourceResponse` and `ServerSentEvent`. This replaces any need for the third-party `sse-starlette` package.

Key pattern for the pipeline stream:

```python
from fastapi.sse import EventSourceResponse, ServerSentEvent

@app.get("/api/pipeline/stream", response_class=EventSourceResponse)
async def stream_pipeline(title: str, desc: str, enable_resolution: bool = True):
    async def generate():
        # Step 1: Classification
        yield ServerSentEvent(data={"stage": "classifying", "message": "Extracting semantic embeddings..."}, event="status")
        classification = app.state.classifier.classify(title, desc)
        yield ServerSentEvent(data={"stage": "classified", "result": classification}, event="result")
        
        # ... more steps ...
        
        yield ServerSentEvent(data={"stage": "complete"}, event="done")
    
    return EventSourceResponse(generate())
```

**IMPORTANT:** Since all core logic (classifier, RAG, LLM calls) is synchronous/blocking, the SSE generator must use `asyncio.to_thread()` to avoid blocking the event loop:

```python
import asyncio

classification = await asyncio.to_thread(app.state.classifier.classify, title, desc)
```

### 2.3 Pydantic Models — The Full Data Contract

Based on codebase analysis, these are the exact Pydantic models needed:

#### Input Models
```python
class TicketRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=500)
    description: str = Field(..., min_length=10, max_length=5000)
    enable_resolution: bool = Field(default=True, description="Run full resolution pipeline")
```

#### Output Models (mapped from existing dict returns)
```python
class ClassificationResult(BaseModel):
    category: str
    department: str
    confidence: float
    priority_suggestion: str
    similar_tickets: list[dict]
    all_scores: dict[str, float]
    method: str  # "centroid" | "llm_judge" | "escalated" | "novel_ticket" | "similarity_search"
    is_novel: bool
    escalate: bool
    llm_rationale: str | None

class TriageResult(BaseModel):
    decision: str  # "AUTO_ROUTE" | "ROUTE_WITH_LLM_ASSIST" | "ESCALATE_LOW_CONFIDENCE" | "ESCALATE_NOVEL"
    rationale: str
    route_to: str
    escalate: bool
    urgency_boost: bool
    urgency_keywords: list[str]

class RAGResult(BaseModel):
    suggested_resolution: str
    similar_ticket_ids: list[str]
    context_used: str

class ResolutionResult(BaseModel):
    resolution_steps: list[str]
    confidence: float
    source_ids: list[str]
    raw_text: str

class JudgeResult(BaseModel):
    correctness: int
    completeness: int
    safety: int
    clarity: int
    overall: float
    critique: str
    safety_gate: str  # "PASS" | "BLOCKED"
    auto_resolve_allowed: bool

class AutomationResult(BaseModel):
    should_automate: bool
    pattern_count: int
    matching_ids: list[str]
    suggested_runbook: str

class PipelineResponse(BaseModel):
    decision_mode: str  # "auto_resolve" | "escalate" | "clarify"
    classification: ClassificationResult
    triage: TriageResult
    rag: RAGResult | None
    resolution: ResolutionResult | None
    judge: JudgeResult | None
    automation: AutomationResult | None
    metadata: dict  # Pipeline timing, model versions, etc.
```

### 2.4 Endpoint Structure (Hybrid Orchestration)

Per CONTEXT.md decisions:

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `GET /api/health` | GET | Health check + model status | `{"status": "ok", "models_loaded": true}` |
| `POST /api/classify` | POST | Standalone classification | `ClassificationResult` |
| `POST /api/retrieve` | POST | Standalone RAG retrieval | `RAGResult` |
| `GET /api/pipeline/stream` | GET | Full pipeline with SSE | `EventSourceResponse` (streams `ServerSentEvent` objects) |
| `POST /api/pipeline/run` | POST | Full pipeline (non-streaming) | `PipelineResponse` |
| `GET /api/feedback` | GET | Retrieve feedback history | `list[FeedbackRow]` |

**Note:** The SSE endpoint uses GET with query params (not POST) because the EventSource browser API only supports GET. The React frontend will use the `EventSource` constructor or `fetch()` with a ReadableStream.

### 2.5 CORS Configuration

The React frontend (Phase 2) will run on a different port. CORS must be configured from day 1:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 3. Dependency Analysis

### New Dependencies Required

| Package | Purpose | Install Command |
|---------|---------|-----------------|
| `fastapi>=0.135.0` | Web framework + native SSE | `pip install "fastapi[standard]"` |
| `uvicorn[standard]` | ASGI server (already installed: v0.42.0) | Already present |

**Key finding:** `uvicorn` v0.42.0 is already installed in the venv. Only `fastapi` needs to be added.

**The `fastapi[standard]` extra** includes uvicorn, httptools, watchfiles, and other production essentials. Since uvicorn is already present, a plain `pip install fastapi` may suffice, but using `[standard]` ensures all recommended dependencies.

### Dependencies NOT Needed

| Package | Reason |
|---------|--------|
| `sse-starlette` | FastAPI 0.135.0+ has native SSE via `fastapi.sse.EventSourceResponse` |
| `pydantic` | Bundled with FastAPI |
| `starlette` | Bundled with FastAPI |

### config.py Streamlit Guard

Lines 16-22 of `config.py` import Streamlit as a fallback for secrets:

```python
if not GROQ_API_KEY:
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
```

This is wrapped in a try/except so it won't crash FastAPI, but it will emit an ImportError warning in logs if Streamlit isn't installed. **Action:** This is safe as-is (the except catches it), but should be annotated with a comment explaining why it exists. Phase 3 (The Purge) will remove it entirely.

---

## 4. Risk Analysis

### Risk 1: Blocking I/O in Async Context
- **Problem:** All core modules use synchronous `requests.post()` for LLM calls (Groq/Ollama). Running these in an async FastAPI endpoint without threading will block the event loop.
- **Mitigation:** Wrap all blocking calls in `asyncio.to_thread()` or use FastAPI's `def` (non-async) endpoints which automatically run in a thread pool. For SSE, `asyncio.to_thread()` is mandatory since the generator must be async.

### Risk 2: ChromaDB Thread Safety
- **Problem:** ChromaDB's PersistentClient may not be fully thread-safe under concurrent requests.
- **Mitigation:** Since this is a prototype/demo (hackathon), concurrent load will be minimal. The lifespan pattern ensures a single client instance. For production, add a threading lock around collection queries.

### Risk 3: Model Loading Time
- **Problem:** `SentenceTransformer('all-MiniLM-L6-v2')` takes 2-5 seconds to load. ChromaDB centroid building adds another 1-2 seconds.
- **Mitigation:** The lifespan startup pattern handles this — models load once before the server accepts connections.

### Risk 4: SSE and Proxy Buffering
- **Problem:** Nginx/reverse proxies may buffer SSE responses, causing delays.
- **Mitigation:** For local development, this is not an issue. For deployment, add `X-Accel-Buffering: no` header.

---

## 5. File Structure Plan

```
/home/devesh/Hackathon/
├── main.py              # [NEW] FastAPI application entry point
├── api/                 # [NEW] API layer
│   ├── __init__.py
│   ├── models.py        # Pydantic request/response models
│   ├── routes/          # Route modules
│   │   ├── __init__.py
│   │   ├── classify.py  # /api/classify endpoint
│   │   ├── pipeline.py  # /api/pipeline/run + /api/pipeline/stream
│   │   ├── retrieve.py  # /api/retrieve endpoint
│   │   └── health.py    # /api/health endpoint
│   └── deps.py          # Dependency injection helpers (get_classifier, etc.)
├── config.py            # [EXISTING - unchanged]
├── core/                # [EXISTING - unchanged]
│   ├── classifier.py
│   ├── rag.py
│   ├── agent.py
│   ├── judge.py
│   ├── feedback.py
│   └── embeddings.py
├── app.py               # [EXISTING - untouched until Phase 3]
└── requirements.txt     # [MODIFIED - add fastapi]
```

**Why `api/` directory:** Separating API concerns from core logic maintains the decoupled architecture. Routes import from `core/` but never modify it. This makes Phase 3 (The Purge) clean — just delete `app.py` and the Streamlit-specific code.

---

## 6. Validation Architecture

### Unit Verification
1. `main.py` starts without errors: `uvicorn main:app --host 0.0.0.0 --port 8000`
2. Swagger UI accessible at `http://localhost:8000/docs`
3. Health endpoint returns `200 OK`
4. `/api/classify` with test ticket returns valid `ClassificationResult` JSON
5. `/api/pipeline/run` triggers full cascade and returns `PipelineResponse`
6. `/api/pipeline/stream` emits SSE events with correct `event:` types
7. All existing Streamlit app still works: `streamlit run app.py` (parallel operation)

### cURL Test Suite

```bash
# Health
curl http://localhost:8000/api/health

# Classify
curl -X POST http://localhost:8000/api/classify \
  -H "Content-Type: application/json" \
  -d '{"title":"VPN not working","description":"Users cannot connect, error 619"}'

# Full Pipeline (non-streaming)
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"title":"VPN not working","description":"Users cannot connect, error 619","enable_resolution":true}'

# SSE Stream
curl -N http://localhost:8000/api/pipeline/stream?title=VPN+not+working&description=Users+cannot+connect
```

---

## RESEARCH COMPLETE

All technical decisions from `01-CONTEXT.md` are implementable. The codebase is well-structured for wrapping — no algorithmic changes to core modules are needed. The primary work is:
1. Install FastAPI
2. Create Pydantic models mirroring existing dict returns
3. Create route handlers that import and call core module classes
4. Use lifespan for model loading and SSE for streaming
5. Handle sync→async bridging with `asyncio.to_thread()`
