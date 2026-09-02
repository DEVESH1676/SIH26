# Phase 1 Research: Calibration & Feedback Foundation

## Objectives
- Understand how confidence is calculated in `core/classifier.py` and what bands are present.
- Identify how to structure the SQLite database for the feedback schema.
- Outline the steps required to plan Phase 1.

## Codebase Analysis
- **`core/classifier.py`**:
  - The current confidence score is a blend of `cosine_similarity` with the centroid (60%) and the agreement ratio from the top 3 direct search results (40%).
  - Method logic uses `config.CONFIDENCE_THRESHOLD`.
  - To test calibration, we will need to load all existing embedded tickets (or a separate split if any, but currently all 150 are in ChromaDB), predict their category, and compare against their known category (metadata).
  - A script (`scripts/calibrate_classifier.py`) can iterate over all stored documents in the vector DB, fetch their `category` metadata, re-run `classify()` (or just the raw predict), and map the result's confidence to bands (>0.75, 0.40–0.75, <0.40).

- **SQLite Feedback Table**:
  - Requires `sqlite3` built-in python module.
  - Can implement this as a core service: `core/feedback.py`.
  - Need a `FeedbackStore` class wrapping the DB connection, creating the schema `CREATE TABLE IF NOT EXISTS resolutions ...` if not exists.
  - Provides a method `log_pipeline_run(ticket_id, category, confidence, resolution_steps, judge_scores, agent_action, human_override, outcome)`

## Dependencies
- Standard library `sqlite3` for the feedback component.
- Existing `chromadb` logic.
- We need access to the 150 generated tickets for the calibration check. Their "ground truth" category is currently stored in their ChromaDB metadata `category`. We can just query `self.collection.get(include=["documents", "metadatas"])` to get the dataset for calibration.

## Risk & Gotchas
- The calibration script must be careful *not* to use the identical ticket embedding to search against itself in the vector search fallback (meaning it might have 100% agreement artificially). To test calibration fairly, it should ignore the exact ticket ID in search results.
- The feedback table creation must handle JSON serialization for `judge_scores`.

## Validation Strategy
- The SQL table must be queried successfully.
- Calibrate script must print clear bands and % accuracy.
