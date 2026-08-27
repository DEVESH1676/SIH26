---
wave: 1
depends_on: []
files_modified: ["scripts/calibrate.py", "core/feedback.py"]
autonomous: true
---

# Phase 1: Calibration & Feedback Foundation

## Goal
Validate classifier confidence thresholds and establish the feedback capture table before building any v3 logic.

## Requirements
- CALIB-01
- FDBK-01

## must_haves
- Script mathematically groups existing tickets by confidence and verifies accuracy is >80% for high confidence.
- SQLite database properly stores JSON stringified arrays/objects and persists on disk.

## Tasks

### T1: SQLite Feedback Storage Core

<task>
<read_first>
- `config.py` (for paths)
</read_first>
<action>
Create `core/feedback.py`.
Add a class `FeedbackStore`:
1. `__init__(self, db_path="data/feedback.db")`: Ensure directory `data/` exists. Connect to sqlite3 database at `db_path`.
2. `_init_db(self)`: create table if not exists `resolutions` with schema exactly:
`ticket_id TEXT, category TEXT, confidence REAL, resolution_steps TEXT, judge_scores TEXT, agent_action TEXT, human_override TEXT, outcome TEXT, created_at TIMESTAMP`
3. `log_run(self, ...args)`: insert into resolutions. For `judge_scores`, use `json.dumps(judge_scores)` if it's a python dict. Use UTC datetime for `created_at`.
Create a simple `if __name__ == "__main__":` test block that creates the table and inserts a dummy row, then queries it to prove it works.
</action>
<acceptance_criteria>
- `python core/feedback.py` exits 0.
- `sqlite3 data/feedback.db ".schema resolutions"` returns the table definition.
</acceptance_criteria>
</task>

### T2: Calibration Verification Script

<task>
<read_first>
- `core/classifier.py`
- `core/embeddings.py`
</read_first>
<action>
Create `scripts/calibrate.py`.
1. Initialize the `TicketClassifier`.
2. Fetch ALL stored data from ChromaDB `collection.get(include=["documents", "metadatas"])`.
3. Iterate over the data. For each item:
   a. Extract true `category` from metadata.
   b. Extract text (document)
   c. Call `clf.classify(title="", description=text)` (we can just pass document as description).
   d. Compare `result["category"]` to true `category`.
   e. Record in buckets: `bands = {"high": {"correct":0, "total":0}, "medium": {"correct":0, "total":0}, "low": {"correct":0, "total":0}}`.
   f. Band logic: high if `confidence > 0.75`, medium if `0.40 <= confidence <= 0.75`, low if `confidence < 0.40`.
4. Print summary metrics: accuracy for each band.
</action>
<acceptance_criteria>
- `python scripts/calibrate.py` runs without errors.
- Output includes clearly labeled accuracy percentages for high, medium, and low bands.
</acceptance_criteria>
</task>
