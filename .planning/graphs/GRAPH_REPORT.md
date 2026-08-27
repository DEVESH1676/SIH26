# Graph Report - /home/devesh/Hackathon  (2026-04-19)

## Corpus Check
- 51 files · ~39,776 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 246 nodes · 412 edges · 43 communities detected
- Extraction: 58% EXTRACTED · 42% INFERRED · 0% AMBIGUOUS · INFERRED: 174 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]

## God Nodes (most connected - your core abstractions)
1. `TicketClassifier` - 30 edges
2. `FeedbackStore` - 23 edges
3. `ResolutionEngine` - 22 edges
4. `ResolutionJudge` - 20 edges
5. `ResolutionAgent` - 20 edges
6. `AutomationDiscoveryAgent` - 20 edges
7. `TriageAgent` - 19 edges
8. `TicketRequest` - 14 edges
9. `PipelineResponse` - 11 edges
10. `PipelineStatusEvent` - 11 edges

## Surprising Connections (you probably didn't know these)
- `load_classifier()` --calls--> `TicketClassifier`  [INFERRED]
  /home/devesh/Hackathon/app.py → /home/devesh/Hackathon/core/classifier.py
- `load_rag_engine()` --calls--> `ResolutionEngine`  [INFERRED]
  /home/devesh/Hackathon/app.py → /home/devesh/Hackathon/core/rag.py
- `load_judge()` --calls--> `ResolutionJudge`  [INFERRED]
  /home/devesh/Hackathon/app.py → /home/devesh/Hackathon/core/judge.py
- `⚡ Nexus AI Ticket Intelligence Platform — v3.0 Streamlit Dashboard with 5-Tab Pr` --uses--> `TicketClassifier`  [INFERRED]
  /home/devesh/Hackathon/app.py → /home/devesh/Hackathon/core/classifier.py
- `lifespan()` --calls--> `TicketClassifier`  [INFERRED]
  /home/devesh/Hackathon/main.py → /home/devesh/Hackathon/core/classifier.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.1
Nodes (42): AgenticLayer, AutomationDiscoveryAgent, Agentic Layer v3.0 — Decoupled Agent Architecture  Three specialized agents form, Accepts a ticket + pre-ranked RAG chunks and generates a structured     step-by-, Post-resolution hook that checks for repeating patterns.     Only fires AFTER a, Accepts a ticket + classification result and produces a routing     decision wit, Thin orchestrator that wraps the three specialized agents.     Maintains backwar, ResolutionAgent (+34 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (27): BaseModel, classify_ticket(), Nexus AI — Standalone Classification Endpoint POST /api/classify — Runs the 4-ti, Standalone classification endpoint.     Runs the 4-tier cascade (novelty → fast, health_check(), Nexus AI — Health Check Endpoint GET /api/health — Returns API status, loaded mo, Returns API health status and loaded model information., AutomationResult (+19 more)

### Community 2 - "Community 2"
Cohesion: 0.16
Nodes (22): PipelineResponse, PipelineStatusEvent, Full pipeline output from the Master Orchestrator.     decision_mode is derived, Streamed during pipeline execution via SSE., Input for classification and pipeline endpoints., TicketRequest, _determine_decision_mode(), Nexus AI — Master Pipeline Endpoints POST /api/pipeline/run    — Full pipeline, (+14 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (11): Check for automation-worthy patterns post-resolution., Legacy-compatible entry point.         Runs TriageAgent + AutomationDiscoveryAge, load_classifier(), load_judge(), load_rag_engine(), render_rubric_bar(), run_full_pipeline(), score_color() (+3 more)

### Community 4 - "Community 4"
Cohesion: 0.13
Nodes (13): Confidence Calibration Check — Phase 1 (CALIB-01)  Validates whether the classif, run_calibration(), Ticket Classifier — v3.0 Cascade Architecture  Classification cascade:   1. Embe, Call Groq free-tier API for classification., Call local Ollama for classification., Classify a ticket through the confidence cascade.          Returns dict with key, Classifies tickets using a confidence-based cascade architecture., Find potentially recurring/duplicate tickets. (+5 more)

### Community 5 - "Community 5"
Cohesion: 0.17
Nodes (12): Return total number of logged runs., clean_csv(), main(), Generate remaining 50 tickets (TKT-2024-00101 to 00150) and merge with batch 1., clean_csv(), main(), print_progress(), Generate 100 additional synthetic IT tickets using qwen2.5-gpu:latest via Ollama (+4 more)

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (5): Compute average embedding per category from stored tickets., get_chroma_collection(), get_embedding_model(), ingest_tickets(), Ingest tickets from a CSV file into ChromaDB.

### Community 7 - "Community 7"
Cohesion: 0.4
Nodes (0): 

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (2): Generate resolution from ranked evidence., Call Groq or Ollama for resolution generation.

### Community 9 - "Community 9"
Cohesion: 0.5
Nodes (2): Log a single pipeline run to the feedback table.          Args:             tick, main()

### Community 10 - "Community 10"
Cohesion: 0.67
Nodes (1): Phase 5 UAT: Test ResolutionJudge independently. Validates JUDGE-01/02/03/04.  T

### Community 11 - "Community 11"
Cohesion: 0.67
Nodes (0): 

### Community 12 - "Community 12"
Cohesion: 0.67
Nodes (0): 

### Community 13 - "Community 13"
Cohesion: 0.67
Nodes (0): 

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): LLM-as-Judge Evaluation Framework (Phase 5)  Evaluates AI-generated resolutions

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Execute triage logic and return routing decision.

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Return all rows as a list of dicts.

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Return rows filtered by category.

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (0): 

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (0): 

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (0): 

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (0): 

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (0): 

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (0): 

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (0): 

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (0): 

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (0): 

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **52 isolated node(s):** `Generate remaining 50 tickets (TKT-2024-00101 to 00150) and merge with batch 1.`, `Generate 100 additional synthetic IT tickets using qwen2.5-gpu:latest via Ollama`, `Nexus AI — Pydantic Data Contracts Every model mirrors the exact dict keys retur`, `Input for classification and pipeline endpoints.`, `Single similar ticket from ChromaDB nearest-neighbour search.` (+47 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 14`** (2 nodes): `test_agents.py`, `check()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (2 nodes): `App.tsx`, `main.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (2 nodes): `StageCard.tsx`, `getIcon()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (2 nodes): `TicketForm.tsx`, `handleSubmit()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (2 nodes): `Badge()`, `badge.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (2 nodes): `cn()`, `button.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (2 nodes): `PillNavbar.tsx`, `handleScroll()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (2 nodes): `utils.ts`, `cn()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (2 nodes): `MainLayout.tsx`, `MainLayout()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (2 nodes): `judge.py`, `LLM-as-Judge Evaluation Framework (Phase 5)  Evaluates AI-generated resolutions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (2 nodes): `Execute triage logic and return routing decision.`, `.run()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (2 nodes): `.get_all()`, `Return all rows as a list of dicts.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (2 nodes): `.get_by_category()`, `Return rows filtered by category.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `test_rag_standalone.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `config.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `eslint.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `pipeline.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `HealthPulse.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `HistoryMock.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `AnalyticsMock.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `GlowingProgressBar.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `AuroraBackground.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `TerminalLogs.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `pipeline.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `smoke.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TicketClassifier` connect `Community 4` to `Community 0`, `Community 1`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.226) - this node is a cross-community bridge._
- **Why does `FeedbackStore` connect `Community 0` to `Community 5`, `Community 9`, `Community 10`, `Community 25`, `Community 26`?**
  _High betweenness centrality (0.188) - this node is a cross-community bridge._
- **Why does `ResolutionEngine` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `TicketClassifier` (e.g. with `⚡ Nexus AI Ticket Intelligence Platform — v3.0 Streamlit Dashboard with 5-Tab Pr` and `Nexus AI Ticket Intelligence Platform — v4.0 API FastAPI backend wrapping the co`) actually correct?**
  _`TicketClassifier` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `FeedbackStore` (e.g. with `Nexus AI Ticket Intelligence Platform — v4.0 API FastAPI backend wrapping the co` and `Load all ML models and resources at startup, clean up at shutdown.`) actually correct?**
  _`FeedbackStore` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `ResolutionEngine` (e.g. with `⚡ Nexus AI Ticket Intelligence Platform — v3.0 Streamlit Dashboard with 5-Tab Pr` and `Nexus AI Ticket Intelligence Platform — v4.0 API FastAPI backend wrapping the co`) actually correct?**
  _`ResolutionEngine` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `ResolutionJudge` (e.g. with `⚡ Nexus AI Ticket Intelligence Platform — v3.0 Streamlit Dashboard with 5-Tab Pr` and `Nexus AI Ticket Intelligence Platform — v4.0 API FastAPI backend wrapping the co`) actually correct?**
  _`ResolutionJudge` has 15 INFERRED edges - model-reasoned connections that need verification._