# Nexus AI Ticket Intelligence Platform

## What This Is

An AI-powered IT ticket routing and resolution system that classifies incoming support tickets, retrieves relevant context via RAG, generates step-by-step resolutions, and applies agentic reasoning to decide whether to auto-resolve, escalate, or suggest automations. Built for enterprise IT helpdesks handling Infrastructure, Application, Security, Database, Network, and Access Management issues.

## Core Value

Every incoming ticket gets classified, routed, and resolved with transparent confidence tracking and safety gates — so low-confidence or unsafe resolutions never auto-execute without human review.

## Requirements

### Validated

<!-- Shipped and confirmed valuable during hackathon MVP (v1.0/v2.0). -->

- ✓ **DATA-01**: System ingests synthetic IT tickets into ChromaDB with embeddings — Phase 1
- ✓ **CLASS-01**: System classifies tickets into 6 categories using centroid cosine similarity — Phase 2
- ✓ **CLASS-02**: System outputs confidence scores with dual-method validation (centroid + search) — Phase 2
- ✓ **RAG-01**: System retrieves top-3 similar past tickets from ChromaDB — Phase 3
- ✓ **RAG-02**: System generates step-by-step resolutions via LLM using retrieved context — Phase 3
- ✓ **AGENT-01**: System escalates tickets below confidence threshold to human review — Phase 4
- ✓ **AGENT-02**: System detects repeat patterns (≥3 similar tickets) and suggests automation — Phase 4
- ✓ **UI-01**: Streamlit dashboard with ticket submission, analytics, and session history — Phase 4

### Active

<!-- Milestone v3.0 scope. -->

- [ ] **CALIB-01**: Confidence calibration check validates classifier thresholds against existing data
- [ ] **FDBK-01**: Feedback capture table stores every pipeline run with judge scores and human overrides
- [ ] **CASC-01**: Cascade classifier with fast centroid path + LLM judge fallback
- [ ] **CASC-02**: Novelty detector flags tickets with no training precedent
- [ ] **RANK-01**: Context ranking scores retrieved chunks on semantic similarity, recency, and outcome
- [ ] **MHOP-01**: Multi-hop retrieval chains ticket results to KB articles via metadata filters
- [ ] **TRIAGE-01**: TriageAgent class decides routing based on confidence gates + sentiment
- [ ] **RESOLVE-01**: ResolutionAgent class generates structured resolution steps from ranked RAG
- [ ] **AUTODISC-01**: AutomationDiscoveryAgent runs post-resolution to suggest automations
- [ ] **JUDGE-01**: LLM-as-Judge rubric scorer evaluates resolutions on correctness/completeness/safety/clarity
- [ ] **JUDGE-02**: Safety hard-gate blocks any resolution with safety score < 3 from auto-resolve
- [ ] **UI-02**: 5-tab Streamlit layout with progressive disclosure of each pipeline stage

### Out of Scope

<!-- Explicit boundaries. -->

- Microservices architecture — Cost; prove intelligence logic first in monolith
- Kafka/Pulsar message bus — Overkill for single-process pipeline
- Managed vector databases (Pinecone, Weaviate) — ChromaDB is sufficient and free
- gRPC service mesh — No inter-service communication needed
- Multi-tenant deployment — Single-instance prototype
- Paid API tiers — Must stay on free Groq tier + local Ollama
- Mobile/native app — Streamlit web-only
- PII detection/masking — Not handling real user data

## Context

- **Origin:** 48-hour hackathon prototype (March 2026), now evolving into enterprise-grade intelligence
- **Current codebase:** ~1,000 LOC Python, monolithic Streamlit app with 4 core modules
- **Data:** 150 synthetic IT tickets in ChromaDB, generated via Ollama
- **Known debt:** `sys.path.append` hacks, CSV filename mismatch in app.py, hardcoded Ollama IP
- **Architecture blueprints:** v2 (industry landscape research) and v3 (enterprise microservices) documents exist as north-star references
- **Codebase map:** `.planning/codebase/` contains 7 structured documents from GSD scan

## Constraints

- **Budget**: $0.00 — all infrastructure must be free/local (Groq free tier, Ollama, ChromaDB)
- **Stack**: Python 3.14, Streamlit, ChromaDB, sentence-transformers, Groq/Ollama
- **LLM**: Groq `llama3-70b-8192` (free tier) + Ollama `qwen2.5-gpu` (local)
- **Embedding**: `all-MiniLM-L6-v2` (384-dim, CPU-compatible)
- **Runtime**: Single-process monolith — no distributed infrastructure

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Monolith over microservices | Zero budget, prove intelligence first | — Pending |
| Groq free tier for LLM-as-Judge | Fast, free, good reasoning | — Pending |
| Direct REST calls to Ollama (bypass LangChain) | LangChain hangs on cloud-routed models | ✓ Good |
| `all-MiniLM-L6-v2` for embeddings | CPU-only, fast, sufficient quality | ✓ Good |
| ChromaDB with SQLite backend | Zero config, persistent, metadata filtering | ✓ Good |
| SQLite feedback table (not ChromaDB) | Structured relational data needs SQL, not vectors | — Pending |
| Cascade classifier (centroid → LLM) | Save LLM tokens on easy tickets | — Pending |
| Safety hard-gate on judge scores | Never auto-resolve unsafe resolutions | — Pending |

## Current Milestone: v4.0 Architectural Decoupling & UI Modernization

**Goal:** Transition from a monolithic Streamlit architecture to a decoupled React + Vite frontend and FastAPI backend builder to support premium UI aesthetics and pure API interaction.

**Target features:**
- Backend Extraction: Wrapping existing AI modules via FastAPI integration
- Frontend Scaffolding: Creating an elite, glassmorphic UI using React + Tailwind
- The Purge: Scouring the codebase of Streamlit components and GUI logic inside python libraries.
- Branch Convergence: Syncing codeframes back into `core` and setting up the true `core/zenith/main` pipeline.

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-08 after milestone v3.0 initialization*
