# Nexus AI Ticket Intelligence Platform — Project Context

## Gemini Added Memories
- **Git Workflow**: Always git commit after work is done. Commit messages must be precise, stating exactly what was done and listing the specific files changed. Avoid complex or mismatched messages.

## Project Overview
Nexus AI is an enterprise-grade IT ticket routing and resolution system. It has transitioned from a monolithic Streamlit app to a **Decoupled Architecture**: a FastAPI backend providing a brain-as-a-service, and a premium React/Vite frontend.

### Core Stack
- **Frontend**: React 18, Vite, Tailwind CSS (located in `frontend-v2/`).
- **Backend**: FastAPI (Python 3.14+).
- **Vector Database**: ChromaDB (Local Persistent).
- **Embeddings**: `all-MiniLM-L6-v2` (Sentence-Transformers).
- **LLM Orchestration**: Direct REST calls to Ollama (local) and Groq API (cloud free tier).
- **Data Storage**: SQLite (for feedback and resolution tracking).

### Key Architectural Patterns
1. **Confidence-Based Cascade**: Managed by `TicketClassifier` in the backend. 
2. **Decoupled Agent Trio**: `TriageAgent`, `ResolutionAgent`, and `AutomationDiscoveryAgent` in `core/agent.py`.
3. **Master SSE Pipeline**: Backend streams real-time updates via Server-Sent Events (SSE) to the frontend.
4. **Architectural Observability**: A "Nexus Blueprint" tab in the UI using Mermaid.js to visualize live logic flows.

---

## Building and Running

### Prerequisites
- Python 3.14+
- Node.js & npm
- Local Ollama instance (running `qwen2.5-gpu:latest`)
- Groq API Key (in `.env`)

### Setup (Backend)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Setup (Frontend)
```bash
cd frontend-v2
npm install
```

### Running the Application
1. **Start Backend**: `uvicorn main:app --host 0.0.0.0 --port 8001`
2. **Start Frontend**: `cd frontend-v2 && npm run dev`

---

## Development Conventions

### Code Structure
- **`main.py`**: FastAPI entry point.
- **`api/routes/`**: API endpoints (Pipeline, Blueprint, Health).
- **`core/`**: Foundational AI logic (Classifier, RAG, Agents).
- **`frontend-v2/`**: The modern React application.
- **`.planning/`**: Structured project documentation using the GSD (Get Shit Done) framework.

### Guidelines
- **Bypass LangChain**: Use direct `requests` to Ollama/Groq for stability.
- **Precision Commits**: Messages must name modified files and specific actions.
- **Validation-First**: Implement Zod validation in the frontend to prevent 422 errors.

---

## Current Status (Milestone v4.0)
- **Phase 1 (Backend Extraction)**: COMPLETE
- **Phase 2 (Frontend Scaffolding)**: COMPLETE
- **Phase 3 (Robustness & State Sync)**: COMPLETE
- **Phase 4 (Architectural Observability)**: COMPLETE
- **Phase 5 (The Purge)**: PLANNED

*Refer to `tillnow.md` for a detailed log of recent changes and `.planning/ROADMAP.md` for upcoming features.*
