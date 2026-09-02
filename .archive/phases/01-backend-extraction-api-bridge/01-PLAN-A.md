---
phase: 1
plan: A
type: foundation
wave: 1
depends_on: []
files_modified:
  - requirements.txt
  - api/__init__.py
  - api/models.py
  - api/deps.py
autonomous: true
requirements:
  - API-01
  - API-02
---

<objective>
Install FastAPI, create Pydantic data contracts mirroring every existing core module return type, and build a dependency injection layer that loads ML models at startup. This is the foundation wave — every other plan depends on these models and helpers existing.
</objective>

<tasks>

<task id="A1" type="command">
<title>Install FastAPI into virtual environment</title>
<read_first>
- requirements.txt
</read_first>
<action>
Run: `source venv/bin/activate && pip install "fastapi[standard]>=0.135.0"`

Then add `fastapi[standard]>=0.135.0` to `requirements.txt` on a new line. Do NOT remove any existing entries — the Streamlit app must continue to work alongside the new API until Phase 3.

The `[standard]` extra bundles uvicorn (already installed v0.42.0), httptools, watchfiles, and websockets.
</action>
<verify>
Run: `source venv/bin/activate && python -c "from fastapi import FastAPI; from fastapi.sse import EventSourceResponse, ServerSentEvent; print('FastAPI OK')"` — must print "FastAPI OK"
</verify>
<acceptance_criteria>
- `pip show fastapi` shows version >= 0.135.0
- `requirements.txt` contains `fastapi[standard]>=0.135.0`
- `python -c "from fastapi.sse import EventSourceResponse"` exits 0
- All existing entries in `requirements.txt` are preserved (streamlit, langchain, etc. still present)
</acceptance_criteria>
</task>

<task id="A2" type="code" files="api/__init__.py">
<title>Create api package directory</title>
<read_first>
- (no existing file — new creation)
</read_first>
<action>
Create directory `api/` at project root with an empty `__init__.py` file. Also create `api/routes/__init__.py`.

```
api/
├── __init__.py          # empty
└── routes/
    └── __init__.py      # empty
```
</action>
<verify>
Run: `python -c "import api; import api.routes; print('api package OK')"` from project root.
</verify>
<acceptance_criteria>
- `api/__init__.py` exists and is importable
- `api/routes/__init__.py` exists and is importable
</acceptance_criteria>
</task>

<task id="A3" type="code" files="api/models.py">
<title>Create Pydantic request/response models</title>
<read_first>
- core/classifier.py (lines 276-287: classify() return dict — 11 fields)
- core/agent.py (lines 106-113: TriageAgent.run() return — 6 fields)
- core/agent.py (lines 192-197: ResolutionAgent.run() return — 4 fields)
- core/agent.py (lines 311-316: AutomationDiscoveryAgent.run() return — 4 fields)
- core/rag.py (lines 187-191: suggest_resolution() return — 3 fields)
- core/judge.py (lines 140-150: _parse_result() return — 8 fields)
- core/feedback.py (lines 50-87: log_run() parameters — 8 fields)
</read_first>
<action>
Create `api/models.py` with every Pydantic model needed for the API. Each model MUST exactly mirror the dict keys returned by the corresponding core module function. Here are the exact models:

```python
from pydantic import BaseModel, Field
from typing import Optional


# ── Request Models ──────────────────────────────────────────
class TicketRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=500, description="Ticket subject line")
    description: str = Field(..., min_length=10, max_length=5000, description="Full ticket description")
    enable_resolution: bool = Field(default=True, description="Run full resolution + judge pipeline")


# ── Classification (from TicketClassifier.classify()) ──────
class SimilarTicket(BaseModel):
    document: str
    category: str
    priority: str
    resolution: str
    department: str
    similarity: float

class ClassificationResult(BaseModel):
    category: str
    department: str
    confidence: float
    priority_suggestion: str
    similar_tickets: list[SimilarTicket]
    all_scores: dict[str, float]
    method: str  # centroid | llm_judge | escalated | novel_ticket | similarity_search
    is_novel: bool
    escalate: bool
    llm_rationale: Optional[str] = None


# ── Triage (from TriageAgent.run()) ────────────────────────
class TriageResult(BaseModel):
    decision: str  # AUTO_ROUTE | ROUTE_WITH_LLM_ASSIST | ESCALATE_LOW_CONFIDENCE | ESCALATE_NOVEL
    rationale: str
    route_to: str
    escalate: bool
    urgency_boost: bool
    urgency_keywords: list[str]


# ── RAG (from ResolutionEngine.suggest_resolution()) ───────
class RAGResult(BaseModel):
    suggested_resolution: str
    similar_ticket_ids: list[str]
    context_used: str


# ── Resolution (from ResolutionAgent.run()) ────────────────
class ResolutionResult(BaseModel):
    resolution_steps: list[str]
    confidence: float
    source_ids: list[str]
    raw_text: str


# ── Judge (from ResolutionJudge.judge()) ───────────────────
class JudgeResult(BaseModel):
    correctness: int
    completeness: int
    safety: int
    clarity: int
    overall: float
    critique: str
    safety_gate: str   # PASS | BLOCKED
    auto_resolve_allowed: bool


# ── Automation (from AutomationDiscoveryAgent.run()) ───────
class AutomationResult(BaseModel):
    should_automate: bool
    pattern_count: int
    matching_ids: list[str]
    suggested_runbook: str


# ── Master Pipeline Response ───────────────────────────────
class PipelineResponse(BaseModel):
    """Full pipeline output. decision_mode is derived from triage + judge results."""
    decision_mode: str  # auto_resolve | escalate | clarify
    classification: ClassificationResult
    triage: TriageResult
    rag: Optional[RAGResult] = None
    resolution: Optional[ResolutionResult] = None
    judge: Optional[JudgeResult] = None
    automation: Optional[AutomationResult] = None
    metadata: dict = Field(default_factory=dict, description="Pipeline timing, model versions")


# ── SSE Event Models ───────────────────────────────────────
class PipelineStatusEvent(BaseModel):
    """Streamed during pipeline execution via SSE."""
    stage: str       # classifying | triaging | retrieving | resolving | judging | automating | complete
    message: str     # Human-readable status message
    progress: float  # 0.0 to 1.0


# ── Health ─────────────────────────────────────────────────
class HealthResponse(BaseModel):
    status: str = "ok"
    models_loaded: bool
    version: str = "4.0.0"
    categories: list[str]
```
</action>
<verify>
Run: `source venv/bin/activate && python -c "from api.models import TicketRequest, ClassificationResult, PipelineResponse, PipelineStatusEvent, HealthResponse; print('All models import OK')"` — must print "All models import OK".
</verify>
<acceptance_criteria>
- `api/models.py` contains classes: TicketRequest, SimilarTicket, ClassificationResult, TriageResult, RAGResult, ResolutionResult, JudgeResult, AutomationResult, PipelineResponse, PipelineStatusEvent, HealthResponse
- `ClassificationResult` has exactly these fields: category, department, confidence, priority_suggestion, similar_tickets, all_scores, method, is_novel, escalate, llm_rationale
- `TriageResult` has exactly these fields: decision, rationale, route_to, escalate, urgency_boost, urgency_keywords
- `PipelineResponse` has `decision_mode` field of type `str`
- `from api.models import PipelineResponse` exits 0
</acceptance_criteria>
</task>

<task id="A4" type="code" files="api/deps.py">
<title>Create dependency injection helpers for shared resources</title>
<read_first>
- core/classifier.py (TicketClassifier __init__ — loads model + centroids)
- core/rag.py (ResolutionEngine __init__ — loads collection + embedding model)
- core/agent.py (TriageAgent, ResolutionAgent, AutomationDiscoveryAgent)
- core/judge.py (ResolutionJudge — stateless)
- core/feedback.py (FeedbackStore — SQLite connection)
</read_first>
<action>
Create `api/deps.py` with FastAPI dependency functions that retrieve pre-loaded resources from `app.state`. These will be used in route handlers via `Depends()`.

```python
from fastapi import Request

from core.classifier import TicketClassifier
from core.rag import ResolutionEngine
from core.agent import TriageAgent, ResolutionAgent, AutomationDiscoveryAgent
from core.judge import ResolutionJudge
from core.feedback import FeedbackStore


def get_classifier(request: Request) -> TicketClassifier:
    return request.app.state.classifier


def get_rag_engine(request: Request) -> ResolutionEngine:
    return request.app.state.rag_engine


def get_triage_agent(request: Request) -> TriageAgent:
    return request.app.state.triage_agent


def get_resolution_agent(request: Request) -> ResolutionAgent:
    return request.app.state.resolution_agent


def get_automation_agent(request: Request) -> AutomationDiscoveryAgent:
    return request.app.state.automation_agent


def get_judge(request: Request) -> ResolutionJudge:
    return request.app.state.judge


def get_feedback_store(request: Request) -> FeedbackStore:
    return request.app.state.feedback_store
```
</action>
<verify>
Run: `source venv/bin/activate && python -c "from api.deps import get_classifier, get_rag_engine, get_judge; print('deps OK')"` — must print "deps OK".
</verify>
<acceptance_criteria>
- `api/deps.py` contains functions: get_classifier, get_rag_engine, get_triage_agent, get_resolution_agent, get_automation_agent, get_judge, get_feedback_store
- Each function takes a `Request` parameter and returns from `request.app.state`
- `from api.deps import get_classifier` exits 0
</acceptance_criteria>
</task>

</tasks>

<verification>
1. FastAPI is installed and importable with SSE support
2. All Pydantic models import without errors
3. All dependency helpers import without errors
4. `requirements.txt` has both old (streamlit) and new (fastapi) dependencies
5. No core/ files were modified
</verification>

<success_criteria>
- `api/models.py` and `api/deps.py` exist and are importable
- FastAPI >= 0.135.0 installed in venv
- Zero changes to any file in the `core/` directory
</success_criteria>

<must_haves>
- Pydantic models exactly mirror the dict keys returned by each core module
- FastAPI native SSE imports available (EventSourceResponse, ServerSentEvent)
- Dependency helpers for all 7 core resources
</must_haves>
