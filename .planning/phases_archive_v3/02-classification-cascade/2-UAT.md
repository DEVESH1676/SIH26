---
status: complete
phase: Classification Cascade + Novelty Detection
source: tillnow.md
started: 2026-04-08T14:43:00Z
updated: 2026-04-08T20:55:00Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: 4
name: Novel Ticket Detection
expected: |
  Submit gibberish or a completely out-of-domain ticket (e.g., "Mow my lawn"). The UI displays a purple badge reading "🆕 NOVEL TICKET".
result: passed (verified via script and manual check)

## Tests

### 1. Fast Path (High Confidence)
expected: |
  Submit a highly typical ticket (e.g. from the historical training set) via the Streamlit UI. The system routes without calling the LLM, and the UI displays a green badge reading "⚡ FAST PATH".
result: passed (verified with literal copy of TKT-2024-00001, confidence 98%, method: centroid)

### 2. LLM Judge (Medium Confidence)
expected: |
  Submit a moderately ambiguous ticket. The UI displays an amber badge reading "🧠 LLM JUDGE" and a callout box showing the LLM judge's rationale for the category switch.
result: passed (verified with "VPN connection failure" scenario, confidence 46.5%, method: llm_judge via Groq llama-3.3-70b-versatile)

### 3. Escalated (Low Confidence)
expected: |
  Submit a vague/ambiguous ticket that lacks specific training precedence. The UI displays a red badge reading "🚨 ESCALATED" and doesn't invoke the LLM Judge.
result: passed (verified with "System is slow" scenario, confidence 37.6%, method: escalated)

### 4. Novel Ticket Detection
expected: |
  Submit gibberish or a completely out-of-domain ticket (e.g., "Mow my lawn"). The UI displays a purple badge reading "🆕 NOVEL TICKET".
result: passed (verified with "asdf jkl;" (15.1% sim) and "Mow my lawn" (13.9% sim), both < 20% novelty threshold)

## Summary

total: 4
passed: 4
issues: 0
pending: 0
skipped: 0

## Gaps
None. Cascade logic is robust and thresholds are correctly calibrated for current training set (50 tickets).
