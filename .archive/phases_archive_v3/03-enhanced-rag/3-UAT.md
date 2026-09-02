# Phase 3 UAT: Enhanced RAG via Context Ranking & Multi-Hop

**Requirement Traceability:** RANK-01, RANK-02, MHOP-01, MHOP-02

## Entry Criteria
- Phase 2 completes successfully.
- `rag.py` has been updated with the `_rank_retrieved_chunks` and multi-hop structure.

## UAT Test Cases

### Test 1: Ranked Chunks (RANK-01, RANK-02)
- **Goal**: Ensure chunks are scored on a Semantic, Recency, and Outcome 60/20/20 split.
- **Verification Method**: Run `rag.suggest_resolution(test_ticket)` in the CLI text execution and observe the new `[Scores:]` debug lines.
- **Expected Outcome**: Past tickets print their Final Score out of 1.0, rather than raw Similarity out of 1.0.

### Test 2: Category Multi-Hop Retrieval (MHOP-01, MHOP-02)
- **Goal**: Ensure the second hop uses the predicted category to fetch additional knowledge.
- **Verification Method**: Check the output of the CLI test for `"## Linked Category DB Insight"` block.
- **Expected Outcome**: Output should show `[KB Category 'X']` showing additional category knowledge that wasn't included in the immediate similarity hits.

## Sign-Off Checklist
- [ ] Test 1 Passed (Ranking metrics visible and computed correctly)
- [ ] Test 2 Passed (Hop 2 results successfully injected into context)
- [ ] Code integrated natively into `app.py` or existing usage without crashing

## Exit Criteria
Once tests pass, update `tillnow.md` and mark Phase 3 COMPLETE.
