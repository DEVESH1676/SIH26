# Testing

## Test Framework

**No test framework is installed or configured.**

- No `pytest`, `unittest`, or any test runner in `requirements.txt`
- No `tests/` directory
- No CI/CD pipeline for automated testing

## Existing Test Approach

Each core module has an inline `if __name__ == "__main__"` test block:

| Module | Test Coverage |
|--------|---------------|
| `core/classifier.py` | 6 hardcoded test tickets with printed classification results |
| `core/rag.py` | 1 hardcoded VPN ticket, prints context + resolution |
| `core/agent.py` | 3 test cases: standard, low-confidence, and recurring ticket |
| `core/embeddings.py` | Runs `ingest_tickets()` on `data/synthetic_tickets.csv` |

**Test pattern:**
```python
if __name__ == "__main__":
    print("Initializing [module]...")
    instance = ModuleClass()
    result = instance.method("test input")
    print(result)
```

These are **manual smoke tests**, not automated assertions. Results require visual inspection.

## Evaluation Module

- `evaluation/__init__.py` exists but is empty
- `evaluation/evaluate.py` and `evaluation/llm_judge.py` are **planned but not implemented**
- The `implementation_plan.md` describes scikit-learn metrics (F1, accuracy, confusion matrix) and LLM-as-judge evaluation, but code hasn't been written

## Test Data

- Synthetic ticket CSV provides the test dataset
- No separate train/test split
- No held-out evaluation set
- Classification accuracy was tested informally (6 manual test cases, 100% reported)

## Test Gaps

- No automated unit tests for any module
- No integration tests for the full pipeline
- No edge case testing (empty inputs, malformed data, ChromaDB failures)
- No performance benchmarks
- No evaluation metrics computed programmatically
