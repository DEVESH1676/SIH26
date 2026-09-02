# Part 1 — Risks & Mitigations

## 1.1 Technical Risks

### Risk 1: iGOT Karmayogi API Availability
**Severity**: CRITICAL
**Impact**: No course catalog = no recommendations = platform unusable
**Details**: The entire recommendation engine depends on iGOT API. If API is unavailable, undocumented, or rate-limited, the platform cannot function.
**Mitigation**:
- Implement aggressive caching (30-min TTL)
- Create a local fallback catalog with popular courses
- Add graceful degradation: show cached courses with "Last synced: X minutes ago"
- Contact MoSPI DIID early for API access documentation
- Build mock API layer that can be swapped with real API

### Risk 2: Large Document Processing
**Severity**: HIGH
**Impact**: PDF/video processing can crash the server with large files
**Details**: Government officials may upload 100+ page PDFs, video recordings of training sessions
**Mitigation**:
- Set strict file size limits (50MB for documents, 200MB for videos)
- Implement async processing with progress tracking
- Use streaming parsers (not full-file loads)
- Add timeout limits per file
- Queue-based processing with Celery/RQ if needed

### Risk 3: LLM API Rate Limits & Costs
**Severity**: HIGH
**Impact**: Competency analysis + quiz generation + subjective evaluation all use LLMs
**Details**: Groq free tier has rate limits. A government-wide deployment will exceed them.
**Mitigation**:
- Implement response caching (same prompt → same cached response)
- Use smaller models for simple tasks, larger for complex reasoning
- Batch LLM calls where possible
- Have Ollama (local) as primary, Groq as fallback
- Implement request queuing with backoff

### Risk 4: Data Privacy Compliance
**Severity**: CRITICAL
**Impact**: Government data requires strict compliance (DPDP Act 2023, MeitY guidelines)
**Details**: Personal data of government officials must be protected
**Mitigation**:
- Encrypt PII at rest (AES-256)
- Encrypt data in transit (TLS 1.3)
- Implement data retention policies (auto-delete after X years)
- Audit logging for all data access
- Role-based data access (department-level isolation)
- Regular security audits

### Risk 5: Database Schema Migration
**Severity**: MEDIUM
**Impact**: Existing ChromaDB and SQLite data will be lost
**Details**: Current data (IT tickets, mock courses) has no value for new platform
**Mitigation**:
- Backup existing data before migration
- Create migration scripts that transform existing data where possible
- Use Alembic for reversible migrations
- Test migration on fresh database first

### Risk 6: Frontend State Management Complexity
**Severity**: MEDIUM
**Impact**: Multiple new views (learner, admin, quiz, upload) increase complexity
**Details**: Adding admin dashboard, quiz engine, file upload, analytics increases UI complexity significantly
**Mitigation**:
- Use React Context + useReducer (already in place) for state
- Implement proper route-based code splitting
- Add TypeScript strict mode from the start
- Write component tests for critical flows

## 1.2 Organizational Risks

### Risk 7: Stakeholder Requirements Drift
**Severity**: HIGH
**Impact**: MoSPI may change requirements during development
**Mitigation**:
- Build MVP with core features first
- Regular demo sessions with stakeholders
- Modular architecture allows adding features without breaking existing ones

### Risk 8: Multi-language Complexity
**Severity**: HIGH
**Impact**: Supporting Hindi + 7 Eighth Schedule languages adds significant complexity
**Mitigation**:
- Start with English + Hindi only
- Use i18n framework (react-i18next) from the start
- LLM can translate between languages, but UI strings need manual translation
- Prioritize based on MoSPI department locations

## 1.3 Operational Risks

### Risk 9: Deployment on Government Cloud
**Severity**: MEDIUM
**Impact**: Government cloud has specific requirements (NIC, CIIE)
**Mitigation**:
- Design cloud-agnostic from the start
- Use Docker for containerization
- Support both on-prem and cloud deployment
- Document all infrastructure requirements early

### Risk 10: Performance at Scale
**Severity**: MEDIUM
**Impact**: Thousands of concurrent learners could slow down the system
**Mitigation**:
- Implement Redis caching for frequent queries
- Use connection pooling for database
- Async processing for heavy LLM calls
- Horizontal scaling support (stateless API design)

## 1.4 Risk Priority Matrix

| Risk | Probability | Impact | Priority |
|------|------------|--------|----------|
| iGOT API availability | High | Critical | P0 |
| Data privacy compliance | Medium | Critical | P0 |
| LLM rate limits | High | High | P1 |
| Large document processing | Medium | High | P1 |
| Frontend complexity | Medium | Medium | P2 |
| Govt. cloud deployment | Low | Medium | P2 |
| Multi-language | Medium | High | P1 |
| Performance at scale | Low | Medium | P3 |
