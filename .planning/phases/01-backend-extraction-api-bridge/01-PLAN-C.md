---
phase: 1
plan: C
type: feature
wave: 3
depends_on:
  - 01-PLAN-A
  - 01-PLAN-B
files_modified:
  - api/routes/pipeline.py
  - main.py
autonomous: true
requirements:
  - API-01
  - API-02
---

<objective>
Create the Master Orchestrator endpoints (POST /api/pipeline/run and GET /api/pipeline/stream with SSE) and the FastAPI application entry point (main.py) that wires everything together with lifespan-managed model loading. This is the capstone — once this plan executes, the full API is live.
</objective>

<tasks>

<task id="C1" type="code" files="api/routes/pipeline.py">
<title>Create master pipeline endpoints (POST run + GET SSE stream)</title>
<read_first>
- app.py (lines 770-840: run_full_pipeline() — the exact 7-step execution chain)
- core/classifier.py (TicketClassifier.classify())
- core/agent.py (TriageAgent.run(), ResolutionAgent.run(), AutomationDiscoveryAgent.run())
- core/rag.py (ResolutionEngine.suggest_resolution(), ResolutionEngine._rank_retrieved_chunks())
- core/judge.py (ResolutionJudge.judge())
- api/models.py (all response models + PipelineResponse + PipelineStatusEvent)
- api/deps.py (all dependency getters)
</read_first>
<action>
Create `api/routes/pipeline.py` with two endpoints:

**Endpoint 1: `POST /api/pipeline/run`** — Full pipeline, non-streaming. Returns complete `PipelineResponse`.

**Endpoint 2: `GET /api/pipeline/stream`** — Full pipeline with SSE streaming. Yields `ServerSentEvent` objects with `event: status` for progress and `event: result` for each stage result.

The pipeline replicates the exact 7-step chain from app.py's `run_full_pipeline()`:

```python
import asyncio
import time
from collections.abc import AsyncIterable

from fastapi import APIRouter, Depends, Query, Request
from fastapi.sse import EventSourceResponse, ServerSentEvent

import config
from core.classifier import TicketClassifier
from core.rag import ResolutionEngine
from core.agent import TriageAgent, ResolutionAgent, AutomationDiscoveryAgent
from core.judge import ResolutionJudge
from api.models import (
    TicketRequest, ClassificationResult, TriageResult, RAGResult,
    ResolutionResult, JudgeResult, AutomationResult,
    PipelineResponse, PipelineStatusEvent,
)
from api.deps import (
    get_classifier, get_rag_engine, get_triage_agent,
    get_resolution_agent, get_automation_agent, get_judge,
)


router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])


def _determine_decision_mode(triage_result: dict, judge_result: dict | None, confidence: float) -> str:
    """Derive decision_mode per CONTEXT.md escalation formatting rules."""
    if triage_result.get("escalate"):
        return "escalate"
    if confidence < 0.75 and not judge_result:
        return "clarify"
    if judge_result and not judge_result.get("auto_resolve_allowed", True):
        return "escalate"
    return "auto_resolve"


def _run_pipeline_sync(request: Request, title: str, description: str, enable_resolution: bool) -> dict:
    """Synchronous pipeline execution — mirrors app.py run_full_pipeline() exactly."""
    state = request.app.state
    start_time = time.time()

    # Step 1: Classification
    classification = state.classifier.classify(title, description)

    # Step 2: Triage
    ticket = {"title": title, "description": description}
    triage_result = state.triage_agent.run(ticket, classification)

    # Step 3: RAG Retrieval
    rag_result = state.rag_engine.suggest_resolution(title, description)

    # Step 4: Rank chunks for resolution agent
    query_embedding = state.rag_engine.embedding_model.encode(f"{title} {description}").tolist()
    raw_results = state.rag_engine.collection.query(
        query_embeddings=[query_embedding], n_results=6,
        include=["documents", "metadatas", "distances"]
    )
    ranked_chunks = state.rag_engine._rank_retrieved_chunks(raw_results)[:3]

    resolution_result = None
    judge_result = None
    automation_result = None

    if enable_resolution:
        # Step 5: Resolution Agent
        resolution_result = state.resolution_agent.run(ticket, ranked_chunks)

        # Step 6: Judge
        resolution_text = "\n".join(resolution_result.get("resolution_steps", []))
        judge_result = state.judge.judge(
            {"title": title, "description": description, "category": classification.get("category", "Unknown")},
            resolution_text
        )

        # Step 7: Automation Discovery
        automation_result = state.automation_agent.run({
            "title": title, "description": description,
            "category": classification.get("category", "Unknown"),
            "resolution": resolution_text,
        })
    else:
        # Still run automation check without resolution
        automation_result = state.automation_agent.run({
            "title": title, "description": description,
            "category": classification.get("category", "Unknown"),
            "resolution": "",
        })

    elapsed = round(time.time() - start_time, 2)
    decision_mode = _determine_decision_mode(
        triage_result, judge_result, classification.get("confidence", 0)
    )

    llm_provider = f"Groq/{config.GROQ_MODEL}" if config.USE_GROQ else f"Ollama/{config.OLLAMA_MODEL}"

    return {
        "decision_mode": decision_mode,
        "classification": classification,
        "triage": triage_result,
        "rag": rag_result,
        "resolution": resolution_result,
        "judge": judge_result,
        "automation": automation_result,
        "metadata": {
            "elapsed_seconds": elapsed,
            "llm_provider": llm_provider,
            "embedding_model": config.EMBEDDING_MODEL_NAME,
            "enable_resolution": enable_resolution,
        },
    }


@router.post("/run", response_model=PipelineResponse)
async def run_pipeline(ticket: TicketRequest, request: Request) -> PipelineResponse:
    """
    Master Orchestrator — Full pipeline, non-streaming.
    Runs the entire 7-step intelligence cascade and returns a single PipelineResponse.
    Always returns 200 OK — decision_mode field indicates auto_resolve/escalate/clarify.
    """
    result = await asyncio.to_thread(
        _run_pipeline_sync, request, ticket.title, ticket.description, ticket.enable_resolution
    )
    return PipelineResponse(**result)


@router.get("/stream", response_class=EventSourceResponse)
async def stream_pipeline(
    request: Request,
    title: str = Query(..., min_length=3, description="Ticket title"),
    description: str = Query(..., min_length=10, description="Ticket description"),
    enable_resolution: bool = Query(default=True, description="Run full resolution pipeline"),
) -> AsyncIterable[ServerSentEvent]:
    """
    Master Orchestrator — SSE streaming pipeline.
    Streams real-time status events matching the Streamlit Intelligence Pipeline stages:
    - event: status → Progress updates (stage name + human-readable message)
    - event: result → Stage completion with actual data
    - event: done   → Pipeline complete with full PipelineResponse
    """
    state = request.app.state

    # Step 1: Classification
    yield ServerSentEvent(
        data=PipelineStatusEvent(stage="classifying", message="Extracting semantic embeddings...", progress=0.0),
        event="status"
    )
    classification = await asyncio.to_thread(state.classifier.classify, title, description)
    yield ServerSentEvent(data={"stage": "classified", "result": classification}, event="result")

    # Step 2: Triage
    yield ServerSentEvent(
        data=PipelineStatusEvent(stage="triaging", message="Triage agent routing...", progress=0.15),
        event="status"
    )
    ticket = {"title": title, "description": description}
    triage_result = await asyncio.to_thread(state.triage_agent.run, ticket, classification)
    yield ServerSentEvent(data={"stage": "triaged", "result": triage_result}, event="result")

    # Step 3: RAG Retrieval
    yield ServerSentEvent(
        data=PipelineStatusEvent(stage="retrieving", message="Retrieving & ranking historical evidence...", progress=0.30),
        event="status"
    )
    rag_result = await asyncio.to_thread(state.rag_engine.suggest_resolution, title, description)

    # Step 4: Rank chunks
    query_embedding = await asyncio.to_thread(
        state.rag_engine.embedding_model.encode, f"{title} {description}"
    )
    raw_results = await asyncio.to_thread(
        state.rag_engine.collection.query,
        query_embeddings=[query_embedding.tolist()], n_results=6,
        include=["documents", "metadatas", "distances"]
    )
    ranked_chunks = state.rag_engine._rank_retrieved_chunks(raw_results)[:3]
    yield ServerSentEvent(data={"stage": "retrieved", "result": rag_result}, event="result")

    resolution_result = None
    judge_result = None
    automation_result = None

    if enable_resolution:
        # Step 5: Resolution Agent
        yield ServerSentEvent(
            data=PipelineStatusEvent(stage="resolving", message="Resolution agent generating fix...", progress=0.50),
            event="status"
        )
        resolution_result = await asyncio.to_thread(state.resolution_agent.run, ticket, ranked_chunks)
        yield ServerSentEvent(data={"stage": "resolved", "result": resolution_result}, event="result")

        # Step 6: Judge
        yield ServerSentEvent(
            data=PipelineStatusEvent(stage="judging", message="Quality judge evaluating resolution...", progress=0.70),
            event="status"
        )
        resolution_text = "\n".join(resolution_result.get("resolution_steps", []))
        judge_result = await asyncio.to_thread(
            state.judge.judge,
            {"title": title, "description": description, "category": classification.get("category", "Unknown")},
            resolution_text
        )
        yield ServerSentEvent(data={"stage": "judged", "result": judge_result}, event="result")

        # Step 7: Automation Discovery
        yield ServerSentEvent(
            data=PipelineStatusEvent(stage="automating", message="Scanning for automation patterns...", progress=0.85),
            event="status"
        )
        automation_result = await asyncio.to_thread(
            state.automation_agent.run,
            {"title": title, "description": description,
             "category": classification.get("category", "Unknown"),
             "resolution": resolution_text}
        )
        yield ServerSentEvent(data={"stage": "automated", "result": automation_result}, event="result")
    else:
        automation_result = await asyncio.to_thread(
            state.automation_agent.run,
            {"title": title, "description": description,
             "category": classification.get("category", "Unknown"),
             "resolution": ""}
        )

    # Final: Complete
    decision_mode = _determine_decision_mode(
        triage_result, judge_result, classification.get("confidence", 0)
    )

    llm_provider = f"Groq/{config.GROQ_MODEL}" if config.USE_GROQ else f"Ollama/{config.OLLAMA_MODEL}"

    final_response = {
        "decision_mode": decision_mode,
        "classification": classification,
        "triage": triage_result,
        "rag": rag_result,
        "resolution": resolution_result,
        "judge": judge_result,
        "automation": automation_result,
        "metadata": {
            "llm_provider": llm_provider,
            "embedding_model": config.EMBEDDING_MODEL_NAME,
            "enable_resolution": enable_resolution,
        },
    }

    yield ServerSentEvent(
        data=PipelineStatusEvent(stage="complete", message="Pipeline complete", progress=1.0),
        event="status"
    )
    yield ServerSentEvent(data=final_response, event="done")
```

Key design decisions per CONTEXT.md:
1. `decision_mode` field: "auto_resolve" | "escalate" | "clarify" — derived from triage escalation state, judge safety gate, and confidence thresholds
2. Always 200 OK — the `decision_mode` field tells the frontend how to render, not HTTP status codes
3. SSE event types: `status` (progress), `result` (stage data), `done` (final payload) — directly maps to React EventSource handlers
4. Progress values (0.0 to 1.0) enable a progress bar in the React UI
</action>
<verify>
After main.py is created and server is running:

1. Non-streaming test:
```bash
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"title":"VPN not working","description":"Multiple users cannot connect to VPN. Getting error 619. Remote team is affected.","enable_resolution":true}'
```
Expect: JSON with decision_mode, classification, triage, rag, resolution, judge, automation, metadata keys.

2. SSE streaming test:
```bash
curl -N "http://localhost:8000/api/pipeline/stream?title=VPN+not+working&description=Multiple+users+cannot+connect+to+VPN.+Getting+error+619."
```
Expect: Multiple `event: status` lines with progress, `event: result` lines with stage data, final `event: done` with complete payload.
</verify>
<acceptance_criteria>
- `api/routes/pipeline.py` contains `router = APIRouter(prefix="/api/pipeline")`
- POST `/run` endpoint accepts `TicketRequest` and returns `PipelineResponse`
- GET `/stream` endpoint returns `EventSourceResponse` with SSE events
- `_determine_decision_mode()` returns "auto_resolve", "escalate", or "clarify"
- Pipeline execution chain matches app.py's 7-step order: classify → triage → rag → rank → resolve → judge → automate
- All blocking calls use `asyncio.to_thread()`
- SSE yields events with types: "status", "result", "done"
- `from api.routes.pipeline import router` exits 0
</acceptance_criteria>
</task>

<task id="C2" type="code" files="main.py">
<title>Create FastAPI application entry point with lifespan</title>
<read_first>
- config.py (all configuration values)
- core/classifier.py (TicketClassifier — __init__ loads model + centroids)
- core/rag.py (ResolutionEngine — __init__ loads collection + embedding model)
- core/agent.py (TriageAgent, ResolutionAgent, AutomationDiscoveryAgent)
- core/judge.py (ResolutionJudge)
- core/feedback.py (FeedbackStore)
- api/routes/health.py (router)
- api/routes/classify.py (router)
- api/routes/retrieve.py (router)
- api/routes/pipeline.py (router)
</read_first>
<action>
Create `main.py` at the project root `/home/devesh/Hackathon/main.py`:

```python
"""
Nexus AI Ticket Intelligence Platform — v4.0 API
FastAPI backend wrapping the core intelligence modules.
Run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.classifier import TicketClassifier
from core.rag import ResolutionEngine
from core.agent import TriageAgent, ResolutionAgent, AutomationDiscoveryAgent
from core.judge import ResolutionJudge
from core.feedback import FeedbackStore

from api.routes import health, classify, retrieve, pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load all ML models and resources at startup, clean up at shutdown."""
    print("⚡ Nexus AI API — Loading intelligence modules...")

    # Load heavy resources once (mirrors Streamlit's @st.cache_resource)
    app.state.classifier = TicketClassifier()
    app.state.rag_engine = ResolutionEngine()
    app.state.triage_agent = TriageAgent()
    app.state.resolution_agent = ResolutionAgent()
    app.state.automation_agent = AutomationDiscoveryAgent()
    app.state.judge = ResolutionJudge()
    app.state.feedback_store = FeedbackStore()

    print("✓ All modules loaded. API ready.")
    yield
    # Shutdown
    print("⚡ Shutting down Nexus AI API...")
    app.state.feedback_store.close()


app = FastAPI(
    title="Nexus AI — Ticket Intelligence API",
    description="RESTful API wrapping the Nexus AI classification cascade, RAG retrieval, "
                "agent-based triage, and LLM-as-Judge quality evaluation.",
    version="4.0.0",
    lifespan=lifespan,
)

# CORS — allow React frontend in dev (Vite default ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(health.router)
app.include_router(classify.router)
app.include_router(retrieve.router)
app.include_router(pipeline.router)


@app.get("/", include_in_schema=False)
def root():
    return {"message": "Nexus AI API v4.0 — Visit /docs for Swagger UI"}
```

The file must be placed at `/home/devesh/Hackathon/main.py` (same level as `config.py` and `app.py`) so that all `import config` and `from core.X import Y` statements resolve without sys.path hacks.

Key design decisions:
1. `lifespan` pattern for model loading — recommended by FastAPI for ML applications
2. CORS configured for Vite defaults (5173, 3000, 8080) — Phase 2 React app will run on one of these
3. Root `/` redirects users to `/docs` Swagger UI — the "Technical Feasibility" win for the assessment
4. All routers prefixed with `/api/` — clean namespacing for future reverse proxy
</action>
<verify>
Run the server:
```bash
cd /home/devesh/Hackathon && source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000
```
Expected startup output:
```
⚡ Nexus AI API — Loading intelligence modules...
✓ Built centroids for 6 categories: [...]
✓ All modules loaded. API ready.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Then test in another terminal:
```bash
# 1. Root redirect
curl http://localhost:8000/
# Expect: {"message":"Nexus AI API v4.0 — Visit /docs for Swagger UI"}

# 2. Health
curl http://localhost:8000/api/health
# Expect: {"status":"ok","models_loaded":true,...}

# 3. Swagger UI
# Open http://localhost:8000/docs in browser — should show interactive API documentation

# 4. Full pipeline
curl -X POST http://localhost:8000/api/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"title":"VPN not working","description":"Multiple users cannot connect to VPN. Getting error 619."}'
# Expect: Full PipelineResponse JSON with decision_mode field
```
</verify>
<acceptance_criteria>
- `main.py` exists at `/home/devesh/Hackathon/main.py`
- `main.py` contains `app = FastAPI(...)` with title "Nexus AI — Ticket Intelligence API" and version "4.0.0"
- `main.py` contains `@asynccontextmanager` lifespan function loading all 7 resources
- `main.py` includes CORSMiddleware with localhost:5173 in allow_origins
- `main.py` includes all 4 routers: health, classify, retrieve, pipeline
- `uvicorn main:app` starts without import errors
- Swagger UI at `/docs` displays all endpoints
- `curl http://localhost:8000/api/health` returns 200 with `models_loaded: true`
- `app.py` (Streamlit) is NOT modified — both can run simultaneously on different ports
</acceptance_criteria>
</task>

</tasks>

<verification>
1. `uvicorn main:app --host 0.0.0.0 --port 8000` starts successfully
2. Swagger UI at `http://localhost:8000/docs` shows all 6 endpoints
3. `POST /api/classify` returns valid ClassificationResult
4. `POST /api/retrieve` returns valid RAGResult
5. `POST /api/pipeline/run` returns valid PipelineResponse with decision_mode
6. `GET /api/pipeline/stream` emits SSE events with correct event types
7. `GET /api/health` returns models_loaded: true
8. `streamlit run app.py` still works on port 8501 (parallel operation)
9. ZERO modifications to any file in the `core/` directory
</verification>

<success_criteria>
- Complete REST API with 6 endpoints is live and testable via Swagger
- SSE pipeline stream emits real-time progress events
- All responses are typed via Pydantic models
- FastAPI auto-generates interactive API documentation
- Existing Streamlit app continues to work unchanged
</success_criteria>

<must_haves>
- main.py at project root with lifespan model loading
- Master orchestrator POST /api/pipeline/run returning PipelineResponse
- SSE streaming GET /api/pipeline/stream with status/result/done events
- CORS configured for React dev server ports
- Swagger UI available at /docs
- decision_mode field in PipelineResponse (auto_resolve | escalate | clarify)
</must_haves>
