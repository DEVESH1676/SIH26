---
phase: 1
slug: calibration-feedback-foundation
date: 2026-04-08
context_size: 1500
---

# Validation Architecture: Phase 1

This document implements the Nyquist Validation framework for Phase 1.

## 1. Domain Boundary
- Calibration script (`scripts/calibrate.py`) checks accuracy of existing classification thresholds.
- SQLite feedback database (`core/feedback.py` and `data/feedback.db`) tracks historical inference/execution loops.

## 2. Invariants & Edge Cases
- **Self-Similarity Bias:** The calibration test must not trivially match a document to itself when doing nearest-neighbor search. N-result search should filter out the exact ID being queried.
- **SQLite Concurrency:** SQLite must be thread-safe for basic writes. Using default settings is fine for this prototype.

## 3. Tooling Validation
- Run `python scripts/calibrate.py` to see the distribution outputs.
- Query SQLite directly via CLI: `sqlite3 data/feedback.db "SELECT * FROM resolutions;"`

## 4. Verification Dimensions
- **D4 (State Change):** Creates `data/feedback.db`.
- **D5 (Error Paths):** Handled graceful initialization when vectors or records are missing.
- **D8 (Nyquist Complete):** Checked all edges.
