# Part 1 — Files to Delete/Archive

## 1.1 Delete These Files

### `api/routes/blueprint.py`
**Reason**: Returns IT ticket pipeline flow — completely irrelevant to learning platform. The architecture visualization can be rebuilt later as a learning-flow diagram if needed.

### `api/routes/history.py`
**Reason**: Returns IT ticket history with confidence scores and resolution steps. The entire history functionality needs to be rewritten for learning history. Better to delete and recreate properly in the new schema.

### `core/classifier.py`
**Reason**: Contains `CompetencyAnalyzer` which is IT-ticket-oriented. The competency analysis for MoSPI needs a complete rebuild with statistical domain knowledge. However, the LLM-calling pattern (`_call_llm`) is reusable.

### `scripts/calibrate.py`
**Reason**: Confidence calibration for IT ticket classifier — irrelevant to learning platform.

### `scripts/ingest_kaggle.py`
**Reason**: Ingests IT ticket Kaggle datasets — completely irrelevant. Replace with iGOT catalog sync.

### `scripts/test_agents.py`
**Reason**: Tests IT-focused agents. Will be replaced with learning-specific tests.

### `scripts/test_cascade.py`
**Reason**: Tests IT ticket cascade classifier. Irrelevant.

### `scripts/test_feedback.py`
**Reason**: Tests IT ticket feedback loop. Will be replaced.

### `scripts/test_judge.py`
**Reason**: Tests IT ticket LLM judge. Will be replaced.

### `test_rag_standalone.py`
**Reason**: Tests IT-focused RAG. Will be replaced.

### `data/dataset-tickets-*` (ALL CSV files in data/)
**Reason**: IT ticket datasets — completely irrelevant to statistical competency learning.

### `data/synthetic_tickets_merged.csv`
**Reason**: Synthetic IT tickets — irrelevant.

### `data/generate_100.py`, `data/generate_100_batch2.py`, `data/generate_data.py`
**Reason**: IT ticket data generators — irrelevant.

### `data/mock_igot_catalog.csv`
**Reason**: While related to iGOT, this is a mock. Will be replaced with real API integration.

### `data/generate_igot_courses.py`
**Reason**: Mock iGOT course generator. Will be replaced with real iGOT API sync.

### `data/feedback.db`
**Reason**: IT ticket feedback database — schema completely wrong for learning platform.

## 1.2 Archive/Keep (Partial Reuse)

### `core/rag.py`
**Keep but rewrite**: `_call_llm()` function is reusable. `CourseRecommender` needs iGOT integration. `QuizGenerator` needs file processing support. Keep the file, replace the content.

### `core/judge.py` (SubjectiveAssessor)
**Keep largely as-is**: The LLM-as-Judge pattern is directly applicable to evaluating learner answers. May need minor prompt adjustments for educational context.

### `core/embeddings.py`
**Keep but modify**: Embedding model and ChromaDB infrastructure is reusable. Replace `COLLECTION_NAME`, `ingest_courses()`, and `embed_document_chunks()`.

### `api/models.py`
**Rewrite**: Most models are IT-specific. The structure/Pydantic patterns can be reused but content must be completely rewritten.

### `api/deps.py`
**Modify**: Dependency injection pattern is sound. Update to inject new services (auth, igot_client, file_processor, analytics).

### `main.py`
**Rewrite**: FastAPI app structure is good. Replace all route registrations, lifespan initialization, and CORS settings. Keep the app scaffolding pattern.

### `config.py`
**Replace with new config**: The pattern (env vars + settings) is good. Replace all content with MoSPI learning settings.

### `requirements.txt`
**Rewrite**: Remove unused packages (langchain*, plotly). Add new packages (file processing, auth, deployment).

## 1.3 Frontend Files to Delete

### `frontend-v2/src/pages/Blueprint.tsx`
**Reason**: Shows IT pipeline architecture — irrelevant. Can be rebuilt as "System Architecture" view for admin if needed.

### `frontend-v2/src/components/Architecture/*`
**Reason**: Mermaid graph and term inspector for IT ticket pipeline — irrelevant.

### `frontend-v2/src/components/Analytics/AnalyticsMock.tsx`
**Reason**: Mock IT analytics — needs complete rewrite with real learning data.

### `frontend-v2/src/components/History/HistoryMock.tsx`
**Reason**: Mock history — replaced by new History component with learning data.

### `frontend-v2/src/components/History/History.tsx`
**Reason**: IT ticket history — needs complete rewrite for learning history.

### `frontend-v2/src/components/Pipeline/IntelligenceFeed.tsx`
**Reason**: IT pipeline feed — needs rewriting for learning pipeline stages.

### `frontend-v2/src/components/Pipeline/StageCard.tsx`
**Reason**: IT pipeline stage cards — needs learning-specific stages and rendering.

### `frontend-v2/src/components/Pipeline/SystemReadiness.tsx`
**Reason**: IT system readiness — needs learning platform readiness indicators.

### `frontend-v2/src/components/Pulse/HealthPulse.tsx`
**Reason**: IT health metrics — needs learning platform metrics.

### `frontend-v2/src/components/Command/GlowingProgressBar.tsx`
**KEEP**: Generic progress bar — reusable as-is with different labels.

### `frontend-v2/src/components/Command/ProfileForm.tsx`
**Rewrite**: Form needs additional fields (department, education, experience, training history). Keep the validation pattern.

### `frontend-v2/src/components/Visuals/TerminalLogs.tsx`
**KEEP**: Generic terminal logs — reusable with learning-specific messages.

### `frontend-v2/src/hooks/usePipeline.tsx`
**Rewrite**: Pipeline stages need to change to learning stages. SSE pattern is reusable.

### `frontend-v2/src/types/pipeline.ts`
**Rewrite**: Types need learning-specific stages and data structures.

### `frontend-v2/src/components/Navigation/PillNavbar.tsx`
**Rewrite**: Navigation items need to change (Learning Plans → Learning Hub, Analytics → Dashboard, Blueprint → Architecture).

### `frontend-v2/src/layouts/MainLayout.tsx`
**Modify**: Change branding from "Nexus Intelligence Platform" to "MoSPI AI Learning Platform". Keep the layout pattern.

### `frontend-v2/src/App.tsx`
**Rewrite**: Add new routes (auth, learner dashboard, admin dashboard, quiz, upload).

### `frontend-v2/src/components/Visuals/AuroraBackground.tsx`, `NeuralParticles.tsx`, `HoverBorderCard.tsx`
**KEEP**: These are generic visual components — reusable as-is.

### `frontend-v2/src/components/ui/*`
**KEEP**: shadcn/ui components — reusable as-is.

### `frontend-v2/src/config/theme.ts`, `src/index.css`, `src/styles/theme.css`
**KEEP**: Styling infrastructure — modify color scheme for MoSPI branding.

### `frontend-v2/src/lib/utils.ts`
**KEEP**: Generic utilities — reusable as-is.

### `frontend-v2/tests/` (both test files)
**Delete and recreate**: Tests are IT-specific. Will be rewritten with learning platform tests.

## 1.4 Planning & Metadata Files

### `.planning/phases_archive_v3/`
**Archive**: Historical phase plans — keep for reference but don't modify.

### `.planning/phases/01-*` through `04-*`
**Archive**: v4.0 phase plans — complete and irrelevant for v5.0.

### `artifacts/v1.md`, `artifacts/v2.md`
**Archive**: Historical implementation plans.

### `tillnow.md`
**Archive**: Development log — keep as reference.

### `GEMINI.md`
**Archive**: Project context — needs complete rewrite for learning platform.
