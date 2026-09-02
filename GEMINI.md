# MoSPI AI Learning Platform — Project Context

## Gemini Added Memories
- **Git Workflow**: Always git commit after work is done. Commit messages must be precise, stating exactly what was done and listing the specific files changed. Avoid complex or mismatched messages.
- **Rules Adherence**: Always respect `.agents/rules/` for phase-driven development, workspace collaboration, and progress tracking.

## Project Overview
The MoSPI AI Learning Platform is an intelligent learning management system built for the Ministry of Statistics and Programme Implementation. It evaluates user competency profiles (based on the FRAC model), identifies skill gaps, recommends iGOT training courses, and conducts dynamically generated subjective and objective assessments.

### Core Stack
- **Frontend**: React 18, Vite, Tailwind CSS (located in `frontend-v2/`).
- **Backend**: FastAPI (Python 3.14+).
- **Vector Database**: ChromaDB (Local Persistent - stores course catalog).
- **Embeddings**: `all-MiniLM-L6-v2` (Sentence-Transformers).
- **LLM Orchestration**: Direct REST calls to Ollama (local) and Groq API (cloud free tier).
- **Data Storage**: SQLite (`learner_progress.db` for tracking competency profiles and learning events).

### Key Architectural Patterns
1. **Competency-Based Evaluation**: Managed by `CompetencyAnalyzer` (evaluates FRAC Domain, Behavioral, and Functional skills).
2. **Learning Agents**: `ProfileAgent`, `PathwayAgent`, and `AssessmentAgent` in `core/agent.py`.
3. **Master SSE Pipeline**: Backend streams real-time updates via Server-Sent Events (SSE) to the frontend learning dashboard.
4. **MoSPI LMS Architecture Blueprint**: Visualized in the frontend admin dashboard using Mermaid.js.

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
- **`api/routes/`**: API endpoints (Pipeline, Assessment, Health).
- **`core/`**: Foundational AI logic (CompetencyAnalyzer, CourseRecommender, Agents).
- **`frontend-v2/`**: The modern React application with LMS dashboards.
- **`.planning/`**: Structured project documentation using the GSD framework.

### Guidelines
- **Bypass LangChain**: Use direct `requests` to Ollama/Groq for stability.
- **Precision Commits**: Messages must name modified files and specific actions.
- **Validation-First**: Implement Zod validation in the frontend.

---

## Current Status (v5.0 Migration)
- **Phase 1 (Gap Assessment & Core Migration)**: COMPLETE (Transitioned from legacy IT ticketing to MoSPI LMS, implemented core AI agents).
- **Phase 5 (The Purge)**: IN PROGRESS (Cleaning up legacy IT ticket logic, tests, and data).
