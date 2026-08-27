"""
Phase 4 UAT: Test all 3 agents independently with mock inputs.
Validates TRIAGE-01/02, RESOLVE-01/02, AUTODISC-01/02.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent import TriageAgent, ResolutionAgent, AutomationDiscoveryAgent

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
print("  Phase 4 UAT — Agent Verification Suite")
print("=" * 70)

# ──────────────────────────────────────────────────────────────
# TEST 1: TriageAgent (TRIAGE-01, TRIAGE-02)
# ──────────────────────────────────────────────────────────────
print("\n── Test 1: TriageAgent ──")
triage = TriageAgent()

# 1a: High confidence → AUTO_ROUTE, no escalation
t1 = triage.run(
    {"title": "Printer toner empty", "description": "Floor 3 HP laserjet needs cyan toner."},
    {"confidence": 0.88, "category": "Infrastructure", "method": "centroid",
     "is_novel": False, "department": "Cloud Platform Engineering"},
)
check("High confidence auto-routes", t1["decision"] == "AUTO_ROUTE" and not t1["escalate"])

# 1b: Low confidence → ESCALATE
t2 = triage.run(
    {"title": "Help", "description": "Something is broken."},
    {"confidence": 0.25, "category": "Application", "method": "escalated",
     "is_novel": False, "department": "Application Support Team"},
)
check("Low confidence escalates", t2["decision"] == "ESCALATE_LOW_CONFIDENCE" and t2["escalate"])

# 1c: Novel ticket → ESCALATE_NOVEL
t3 = triage.run(
    {"title": "Mow the lawn", "description": "Office garden needs maintenance."},
    {"confidence": 0.05, "category": "Unknown", "method": "novel_ticket",
     "is_novel": True, "department": "General Support L1"},
)
check("Novel ticket escalates", t3["decision"] == "ESCALATE_NOVEL" and t3["escalate"])

# 1d: Medium confidence → ROUTE_WITH_LLM_ASSIST
t4 = triage.run(
    {"title": "VPN issue", "description": "Users cannot connect to VPN."},
    {"confidence": 0.55, "category": "Network", "method": "llm_judge",
     "is_novel": False, "department": "Network Operations Center (NOC)"},
)
check("Medium confidence LLM-assisted route", t4["decision"] == "ROUTE_WITH_LLM_ASSIST" and not t4["escalate"])

# 1e: Urgency keyword detection (TRIAGE-02)
t5 = triage.run(
    {"title": "CRITICAL outage", "description": "Production database is DOWN and URGENT."},
    {"confidence": 0.80, "category": "Database", "method": "centroid",
     "is_novel": False, "department": "Database Administration (DBA)"},
)
check("Urgency keywords detected", t5["urgency_boost"] and len(t5["urgency_keywords"]) >= 2,
      f"Got: urgency_boost={t5['urgency_boost']}, keywords={t5['urgency_keywords']}")

# 1f: Result has required keys (TRIAGE-01)
required_keys = {"decision", "rationale", "route_to", "escalate"}
check("TriageAgent returns required keys", required_keys.issubset(set(t1.keys())),
      f"Missing: {required_keys - set(t1.keys())}")


# ──────────────────────────────────────────────────────────────
# TEST 2: ResolutionAgent (RESOLVE-01, RESOLVE-02)
# ──────────────────────────────────────────────────────────────
print("\n── Test 2: ResolutionAgent ──")
resolver = ResolutionAgent()

# 2a: With ranked chunks → generates steps + confidence
mock_chunks = [
    {
        "id": "TKT-MOCK-001", "document": "VPN connection fails for remote users",
        "metadata": {"resolution": "Restarted VPN concentrator and restored backup."},
        "semantic": 0.85, "recency": 0.6, "outcome": 1.0, "final_score": 0.83,
    },
    {
        "id": "TKT-MOCK-002", "document": "VPN timeout on Windows",
        "metadata": {"resolution": "Updated VPN client and adjusted timeout settings."},
        "semantic": 0.70, "recency": 0.4, "outcome": 0.8, "final_score": 0.66,
    },
]

r1 = resolver.run(
    {"title": "VPN disconnects every 5 min", "description": "Error 619 for jdoe."},
    mock_chunks,
)
check("Resolution has steps", len(r1["resolution_steps"]) > 0,
      f"Got {len(r1['resolution_steps'])} steps")
check("Resolution confidence > 0", r1["confidence"] > 0,
      f"Got confidence={r1['confidence']}")
check("Resolution tracks source IDs", len(r1["source_ids"]) == 2,
      f"Got {len(r1['source_ids'])} source IDs")

# 2b: Empty chunks → graceful fallback
r2 = resolver.run({"title": "Mystery", "description": "Unknown issue."}, [])
check("Empty chunks returns fallback", r2["confidence"] == 0.0 and len(r2["resolution_steps"]) > 0)

# 2c: Result has required keys (RESOLVE-01)
required_keys_res = {"resolution_steps", "confidence", "source_ids", "raw_text"}
check("ResolutionAgent returns required keys", required_keys_res.issubset(set(r1.keys())),
      f"Missing: {required_keys_res - set(r1.keys())}")


# ──────────────────────────────────────────────────────────────
# TEST 3: AutomationDiscoveryAgent (AUTODISC-01, AUTODISC-02)
# ──────────────────────────────────────────────────────────────
print("\n── Test 3: AutomationDiscoveryAgent ──")
discovery = AutomationDiscoveryAgent()

# 3a: Known recurring category → should find matches
a1 = discovery.run({
    "title": "VPN connection fails for remote users",
    "description": "Users are unable to establish VPN connections, receiving error 619.",
    "category": "Network",
    "resolution": "Restarted concentrator.",
})
check("Automation discovery returns valid result",
      isinstance(a1["should_automate"], bool) and isinstance(a1["pattern_count"], int))
check("Automation returns matching_ids list", isinstance(a1["matching_ids"], list))

# 3b: Unknown/novel category → should NOT suggest automation
a2 = discovery.run({
    "title": "Alien contact detected",
    "description": "Strange signals from the server room.",
    "category": "Unknown",
    "resolution": "Investigated and found nothing.",
})
check("Unknown category does not auto-suggest", not a2["should_automate"],
      f"Got should_automate={a2['should_automate']}, count={a2['pattern_count']}")

# 3c: Result has required keys (AUTODISC-01)
required_keys_auto = {"should_automate", "pattern_count", "matching_ids", "suggested_runbook"}
check("AutomationDiscoveryAgent returns required keys", required_keys_auto.issubset(set(a1.keys())),
      f"Missing: {required_keys_auto - set(a1.keys())}")


# ──────────────────────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────────────────────
print(f"\n{'=' * 70}")
print(f"  Results: {PASS} PASSED, {FAIL} FAILED out of {PASS + FAIL} tests")
print(f"{'=' * 70}")

if FAIL == 0:
    print("  🎉 ALL TESTS PASSED — Phase 4 UAT COMPLETE")
else:
    print(f"  ⚠️  {FAIL} test(s) failed. Review above.")
