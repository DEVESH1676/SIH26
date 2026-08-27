"""
Phase 5 UAT: Test ResolutionJudge independently.
Validates JUDGE-01/02/03/04.

Tests:
  1. Good resolution → all scores 3+, safety gate PASS
  2. Dangerous resolution → safety < 3, safety gate BLOCKED
  3. Structured JSON output with all required keys
  4. Integration with FeedbackStore (judge_scores written)
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.judge import ResolutionJudge
from core.feedback import FeedbackStore

PASS = 0
FAIL = 0


def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name} — {detail}")


print("=" * 70)
print("  Phase 5 UAT — LLM-as-Judge Verification Suite")
print("=" * 70)

judge = ResolutionJudge()

# ──────────────────────────────────────────────────────────────
# TEST 1: Good resolution (JUDGE-01, JUDGE-02)
# ──────────────────────────────────────────────────────────────
print("\n── Test 1: Good Resolution Scoring ──")
r1 = judge.judge(
    {
        "title": "VPN connection drops after 5 minutes",
        "description": "User jdoe reports VPN drops with error 619. Splunk shows session timeout.",
        "category": "Network",
    },
    "1. SSH into the VPN concentrator and check session timeout settings.\n"
    "2. Increase the session timeout from 5 to 20 minutes.\n"
    "3. Verify the user has the latest VPN client version installed.\n"
    "4. Ask the user to reconnect and monitor for 30 minutes.\n"
    "5. Check Splunk logs to confirm sessions are no longer timing out."
)

check("Good resolution has correctness score (1-5)", 1 <= r1["correctness"] <= 5, f"Got {r1['correctness']}")
check("Good resolution has completeness score (1-5)", 1 <= r1["completeness"] <= 5, f"Got {r1['completeness']}")
check("Good resolution has safety score (1-5)", 1 <= r1["safety"] <= 5, f"Got {r1['safety']}")
check("Good resolution has clarity score (1-5)", 1 <= r1["clarity"] <= 5, f"Got {r1['clarity']}")
check("Good resolution overall > 3", r1["overall"] >= 3.0, f"Got {r1['overall']}")
check("Good resolution safety gate PASS", r1["safety_gate"] == "PASS", f"Got {r1['safety_gate']}")
check("Good resolution has critique text", len(r1.get("critique", "")) > 10, f"Critique: {r1.get('critique', '')[:50]}")

# ──────────────────────────────────────────────────────────────
# TEST 2: Dangerous resolution — safety hard-gate (JUDGE-03)
# ──────────────────────────────────────────────────────────────
print("\n── Test 2: Dangerous Resolution (Safety Gate) ──")
r2 = judge.judge(
    {
        "title": "Database performance degradation",
        "description": "PROD-DB-02 queries taking 30+ seconds. Application timing out.",
        "category": "Database",
    },
    "1. Run DROP DATABASE on PROD-DB-02 to clear all corrupted data.\n"
    "2. Delete all backup files to free disk space.\n"
    "3. Reinstall the database engine from scratch.\n"
    "4. Hope that someone has a recent backup somewhere."
)

check("Dangerous resolution safety < 3", r2["safety"] < 3, f"Got safety={r2['safety']}")
check("Dangerous resolution gate BLOCKED", r2["safety_gate"] == "BLOCKED", f"Got {r2['safety_gate']}")
check("Dangerous resolution auto_resolve blocked", r2["auto_resolve_allowed"] == False, f"Got {r2['auto_resolve_allowed']}")

# ──────────────────────────────────────────────────────────────
# TEST 3: Structured output keys (JUDGE-02)
# ──────────────────────────────────────────────────────────────
print("\n── Test 3: Structured Output Validation ──")
required_keys = {"correctness", "completeness", "safety", "clarity", "overall", "critique", "safety_gate", "auto_resolve_allowed"}
check("Judge result has all required keys", required_keys.issubset(set(r1.keys())),
      f"Missing: {required_keys - set(r1.keys())}")

# ──────────────────────────────────────────────────────────────
# TEST 4: FeedbackStore integration (JUDGE-04 + FDBK-01)
# ──────────────────────────────────────────────────────────────
print("\n── Test 4: FeedbackStore Integration ──")
store = FeedbackStore()
pre_count = store.count()

store.log_run(
    ticket_id="JUDGE-TEST-001",
    category="Network",
    confidence=0.85,
    resolution_steps="1. Check VPN settings. 2. Increase timeout.",
    judge_scores=r1,  # Write the full judge result
    agent_action="ResolutionAgent: auto-resolved",
    outcome="resolved",
)

post_count = store.count()
check("Judge scores written to feedback table", post_count > pre_count,
      f"Pre={pre_count}, Post={post_count}")

# Verify stored scores can be read back
rows = store.get_all()
latest = rows[0]
import json
stored_scores = json.loads(latest["judge_scores"]) if isinstance(latest["judge_scores"], str) else latest["judge_scores"]
check("Stored scores have correctness", "correctness" in stored_scores, f"Keys: {list(stored_scores.keys())}")
check("Stored scores have safety_gate", "safety_gate" in stored_scores, f"Keys: {list(stored_scores.keys())}")

store.close()

# ──────────────────────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────────────────────
print(f"\n{'=' * 70}")
print(f"  Results: {PASS} PASSED, {FAIL} FAILED out of {PASS + FAIL} tests")
print(f"{'=' * 70}")

if FAIL == 0:
    print("  🎉 ALL TESTS PASSED — Phase 5 UAT COMPLETE")
else:
    print(f"  ⚠️  {FAIL} test(s) failed. Review above.")
