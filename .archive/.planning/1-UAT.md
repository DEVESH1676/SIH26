# UAT Plan: Phase 1 (Calibration & Feedback)

**Status:** Complete
**Date Created:** 2026-04-08

## Test Scenarios

### T1: Feedback Store Integrity (FDBK-01)
**Goal:** Verify that the `FeedbackStore` correctly initializes the SQLite database, handles schema creation gracefully, and successfully performs CRUD operations with JSON-serialized `judge_scores`.
- [x] Initialize FeedbackStore
- [x] Log a fake resolution with JSON judge scores
- [x] Verify the SQLite database file exists at `data/feedback.db`
- [x] Query SQLite directly to confirm record matches input

### T2: Calibration Script Accuracy (CALIB-01)
**Goal:** Verify that `scripts/calibrate.py` buckets all tickets by confidence band and outputs accuracy per band.
- [x] Run `python scripts/calibrate.py`
- [x] Output shows high, medium, and low bands.
- [x] Output verifies that high band > 0.75 accuracy is >= 80%.
