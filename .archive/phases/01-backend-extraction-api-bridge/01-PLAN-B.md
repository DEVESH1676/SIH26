---
phase: 1
plan: B
type: feature
wave: 2
depends_on:
  - 01-PLAN-A
files_modified:
  - api/routes/health.py
  - api/routes/classify.py
  - api/routes/retrieve.py
autonomous: true
requirements:
  - API-01
  - API-02
---

<objective>
Create the modular API endpoints: health check, standalone classification, and standalone RAG retrieval. These are the "granular testing and Human-in-the-loop override" endpoints specified in CONTEXT.md.
</objective>

<tasks>

<task id="B1" type="code" files="api/routes/health.py">
<title>Create health check endpoint</title>
<read_first>
- api/models.py (HealthResponse model)
- api/deps.py (get_classifier dependency)
- config.py (CATEGORIES, EMBEDDING_MODEL_NAME, USE_GROQ, GROQ_MODEL, OLLAMA_MODEL)
</read_first>
<action>
Create `api/routes/health.py` with a `GET /api/health` endpoint:

```python
from fastapi import APIRouter, Request

import config
from api.models import HealthResponse

router = APIRouter(prefix="/api", tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health_check(request: Request) -> HealthResponse:
    """Returns API health status and loaded model information."""
    models_loaded = (
        hasattr(request.app.state, "classifier")
        and request.app.state.classifier is not None
    )
    return HealthResponse(
        status="ok",
        models_loaded=models_loaded,
        version="4.0.0",
        categories=config.CATEGORIES,
    )
```
</action>
<verify>
After main.py is created (Plan C), run:
`curl http://localhost:8000/api/health` — expect `{"status":"ok","models_loaded":true,"version":"4.0.0","categories":[...]}`
</verify>
<acceptance_criteria>
- `api/routes/health.py` contains `router = APIRouter(prefix="/api")`
- `router` has a `GET /health` endpoint returning `HealthResponse`
- Response includes `categories` field populated from `config.CATEGORIES`
- `from api.routes.health import router` exits 0
</acceptance_criteria>
</task>

<task id="B2" type="code" files="api/routes/classify.py">
<title>Create standalone classification endpoint</title>
<read_first>
- core/classifier.py (TicketClassifier.classify() — full return dict at lines 276-287)
- api/models.py (TicketRequest, ClassificationResult)
- api/deps.py (get_classifier)
</read_first>
<action>
Create `api/routes/classify.py` with a `POST /api/classify` endpoint:

```python
import asyncio

from fastapi import APIRouter, Depends

from core.classifier import TicketClassifier
from api.models import TicketRequest, ClassificationResult
from api.deps import get_classifier

router = APIRouter(prefix="/api", tags=["modular"])


@router.post("/classify", response_model=ClassificationResult)
async def classify_ticket(
    ticket: TicketRequest,
    classifier: TicketClassifier = Depends(get_classifier),
) -> ClassificationResult:
    """
    Standalone classification endpoint.
    Runs the 4-tier cascade (novelty → fast path → LLM judge → escalation)
    and returns the structured classification result.
    """
    result = await asyncio.to_thread(
        classifier.classify, ticket.title, ticket.description
    )
    return ClassificationResult(**result)
```

Key design decisions:
- Uses `asyncio.to_thread()` because `classifier.classify()` is synchronous and may trigger blocking LLM calls to Groq/Ollama
- The `ClassificationResult(**result)` unpacking works because the Pydantic model fields exactly mirror the dict keys from `classify()`
- `Depends(get_classifier)` pulls the pre-loaded instance from app.state instead of re-creating it
</action>
<verify>
After main.py is created, run:
```bash
curl -X POST http://localhost:8000/api/classify \
  -H "Content-Type: application/json" \
  -d '{"title":"VPN not working","description":"Multiple users cannot connect to VPN. Getting error 619."}'
```
Expect JSON with keys: category, department, confidence, method, is_novel, escalate, etc.
</verify>
<acceptance_criteria>
- `api/routes/classify.py` contains `router = APIRouter(prefix="/api")`
- Endpoint is `POST /classify` accepting `TicketRequest` body
- Uses `asyncio.to_thread()` for the blocking classify() call
- Returns `ClassificationResult` model
- `from api.routes.classify import router` exits 0
</acceptance_criteria>
</task>

<task id="B3" type="code" files="api/routes/retrieve.py">
<title>Create standalone RAG retrieval endpoint</title>
<read_first>
- core/rag.py (ResolutionEngine.suggest_resolution() — return dict at lines 187-191)
- api/models.py (TicketRequest, RAGResult)
- api/deps.py (get_rag_engine)
</read_first>
<action>
Create `api/routes/retrieve.py` with a `POST /api/retrieve` endpoint:

```python
import asyncio

from fastapi import APIRouter, Depends

from core.rag import ResolutionEngine
from api.models import TicketRequest, RAGResult
from api.deps import get_rag_engine

router = APIRouter(prefix="/api", tags=["modular"])


@router.post("/retrieve", response_model=RAGResult)
async def retrieve_context(
    ticket: TicketRequest,
    rag_engine: ResolutionEngine = Depends(get_rag_engine),
) -> RAGResult:
    """
    Standalone RAG retrieval endpoint.
    Performs multi-hop semantic retrieval and returns ranked evidence
    with an LLM-generated resolution suggestion.
    """
    result = await asyncio.to_thread(
        rag_engine.suggest_resolution, ticket.title, ticket.description
    )
    return RAGResult(**result)
```
</action>
<verify>
After main.py is created, run:
```bash
curl -X POST http://localhost:8000/api/retrieve \
  -H "Content-Type: application/json" \
  -d '{"title":"Database slow","description":"PROD-DB-02 queries taking 30+ seconds"}'
```
Expect JSON with keys: suggested_resolution, similar_ticket_ids, context_used.
</verify>
<acceptance_criteria>
- `api/routes/retrieve.py` contains `router = APIRouter(prefix="/api")`
- Endpoint is `POST /retrieve` accepting `TicketRequest` body
- Uses `asyncio.to_thread()` for the blocking suggest_resolution() call
- Returns `RAGResult` model
- `from api.routes.retrieve import router` exits 0
</acceptance_criteria>
</task>

</tasks>

<verification>
1. All three route modules import without errors
2. Each router has the correct prefix `/api`
3. Each endpoint uses `asyncio.to_thread()` for blocking core logic calls
4. Pydantic model unpacking (`**result`) works because model fields match dict keys exactly
5. No core/ files were modified
</verification>

<success_criteria>
- 3 route files created: health.py, classify.py, retrieve.py
- Each endpoint uses dependency injection from `api/deps.py`
- All use async handlers with `asyncio.to_thread()` for sync core calls
</success_criteria>

<must_haves>
- Health endpoint reports model status and categories from config
- Classify endpoint runs full 4-tier cascade and returns typed JSON
- Retrieve endpoint runs multi-hop RAG and returns evidence + resolution
</must_haves>
