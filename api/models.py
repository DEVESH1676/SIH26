"""
Nexus AI — Pydantic Data Contracts
Every model mirrors the exact dict keys returned by core modules.
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# ── Request Models ──────────────────────────────────────────
class TicketRequest(BaseModel):
    """Input for classification and pipeline endpoints."""
    title: str = Field(..., min_length=3, max_length=500, description="Ticket subject line")
    description: str = Field(..., min_length=10, max_length=5000, description="Full ticket description")
    enable_resolution: bool = Field(default=True, description="Run full resolution + judge pipeline")


# ── Classification (from TicketClassifier.classify()) ──────
class SimilarTicket(BaseModel):
    """Single similar ticket from ChromaDB nearest-neighbour search."""
    document: str
    category: str
    priority: str
    resolution: str
    department: str
    similarity: float


class ClassificationResult(BaseModel):
    """
    Output of the 4-tier classification cascade.
    Fields mirror core/classifier.py lines 276-287 and 207-218.
    """
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
    """
    Output of the Triage Agent decision tree.
    Fields mirror core/agent.py lines 106-113.
    """
    decision: str  # AUTO_ROUTE | ROUTE_WITH_LLM_ASSIST | ESCALATE_LOW_CONFIDENCE | ESCALATE_NOVEL
    rationale: str
    route_to: str
    escalate: bool
    urgency_boost: bool
    urgency_keywords: list[str]


# ── RAG (from ResolutionEngine.suggest_resolution()) ───────
class RAGResult(BaseModel):
    """
    Output of the RAG multi-hop retrieval pipeline.
    Fields mirror core/rag.py lines 187-191.
    """
    suggested_resolution: str
    similar_ticket_ids: list[str]
    context_used: str


# ── Resolution (from ResolutionAgent.run()) ────────────────
class ResolutionResult(BaseModel):
    """
    Output of the Resolution Agent LLM generation.
    Fields mirror core/agent.py lines 192-197.
    """
    resolution_steps: list[str]
    confidence: float
    source_ids: list[str]
    raw_text: str


# ── Judge (from ResolutionJudge.judge()) ───────────────────
class JudgeResult(BaseModel):
    """
    Output of the LLM-as-Judge quality evaluation.
    Fields mirror core/judge.py lines 132-150.
    """
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
    """
    Output of the Automation Discovery Agent.
    Fields mirror core/agent.py lines 311-316.
    """
    should_automate: bool
    pattern_count: int
    matching_ids: list[str]
    suggested_runbook: str


# ── Master Pipeline Response ───────────────────────────────
class PipelineResponse(BaseModel):
    """
    Full pipeline output from the Master Orchestrator.
    decision_mode is derived from triage + judge results.
    """
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
    """Health check response."""
    status: str = "ok"
    models_loaded: bool
    version: str = "4.0.0"
    categories: list[str]
