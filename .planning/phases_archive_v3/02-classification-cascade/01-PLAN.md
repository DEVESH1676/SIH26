# Phase 2: Classification Cascade

**Requirements covered:**
- **CASC-01**: System routes tickets through fast centroid path (>0.75 confidence → direct route, no LLM call)
- **CASC-02**: System escalates medium-confidence tickets (0.40–0.75) to LLM judge for re-classification
- **CASC-03**: System escalates low-confidence tickets (<0.40) directly without wasting LLM tokens
- **CASC-04**: System detects novel tickets (embedding distance from ALL training examples above threshold) and flags as NOVEL_TICKET before classification

## Steps

1. **Modify `config.py`**
   - Add `MEDIUM_CONFIDENCE_THRESHOLD = 0.40`.
   - Add `NOVELTY_SIMILARITY_THRESHOLD = 0.20`.
   - Ensure `CONFIDENCE_THRESHOLD = 0.75` is kept.

2. **Modify `core/classifier.py`**
   - Add the Groq LLM API call setup to use the API key from config if `config.USE_GROQ` is True, else fallback to Ollama, for the LLM judge.
   - Refactor `classify(title, description)` to:
     - Check distance of top Chromadb result. If `< NOVELTY_SIMILARITY_THRESHOLD` (meaning similarity is low, wait, similarity < 0.20, distance > 0.8), set `is_novel = True` and return instantly.
     - Blended similarity computation remains.
     - If `confidence > 0.75`, fast path (return).
     - If `confidence < 0.40`, escalate directly (return with confidence).
     - If `0.40 <= confidence <= 0.75`, invoke LLM. Ask it to output JSON with `category` and `rationale`. Parse the JSON, update the object, mark `method: llm_judge`.

3. **Modify `core/agent.py`**
   - Refactor the Triage Agent to understand the new `is_novel` flag and the `method` flag to provide accurate escalations.

4. **Modify `app.py`**
   - Under Tab 2, display indicators for "Fast Path", "LLM Judge", "Escalated/Novel" depending on what happened in classification.
   - Use Streamlit badges or success/warning callouts based on `is_novel` or `method`.

## Verification
- Write tests in `scripts/test_cascade.py` or just verify that the calibration sets still work. Moreso, ensure we trigger the LLM properly.
