"""
Test the classification cascade with 4 distinct scenarios:
  1. Standard IT ticket → expected HIGH confidence (fast centroid path)
  2. Ambiguous ticket → expected MEDIUM confidence (LLM judge fires)
  3. Gibberish → expected LOW confidence (direct escalation)
  4. Out-of-domain → expected NOVEL flag

Run: source venv/bin/activate && python scripts/test_cascade.py
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.classifier import TicketClassifier
import config


def run_cascade_tests():
    print("=" * 70)
    print("  CASCADE CLASSIFIER — 4-Scenario Test")
    print(f"  Thresholds: high={config.CONFIDENCE_THRESHOLD}"
          f"  medium={config.MEDIUM_CONFIDENCE_THRESHOLD}"
          f"  novelty={config.NOVELTY_SIMILARITY_THRESHOLD}")
    print("=" * 70)

    clf = TicketClassifier()

    scenarios = [
        {
            "name": "1. Standard IT ticket (expect MEDIUM → LLM judge)",
            "title": "VPN connection failure",
            "desc": "Multiple users in the remote engineering team cannot connect to the corporate VPN. They are seeing error code 619 on Windows 11. This started after the latest Cisco AnyConnect update.",
            "expect_method": "llm_judge",
        },
        {
            "name": "2. Ambiguous ticket (expect LOW → escalated)",
            "title": "System is slow",
            "desc": "Everything is running slowly but I'm not sure if it's the app or the server or the network.",
            "expect_method": "escalated",
        },
        {
            "name": "3. Gibberish (expect NOVEL → novel_ticket)",
            "title": "asdf jkl;",
            "desc": "qwerty uiop zxcv bnm 12345 random words no meaning.",
            "expect_method": "novel_ticket",
        },
        {
            "name": "4. Out-of-domain (expect NOVEL → novel_ticket)",
            "title": "Need to mow my lawn",
            "desc": "The grass in my backyard is getting really tall and I need someone to come mow it before the HOA fines me.",
            "expect_method": "novel_ticket",
        },
    ]

    results = []
    for s in scenarios:
        print(f"\n{'─' * 60}")
        print(f"  {s['name']}")
        print(f"  Title: \"{s['title']}\"")
        print(f"{'─' * 60}")

        result = clf.classify(s["title"], s["desc"])

        method = result["method"]
        conf = result["confidence"]
        cat = result["category"]
        is_novel = result.get("is_novel", False)
        escalate = result.get("escalate", False)
        llm_rationale = result.get("llm_rationale")

        # Tag display
        novel_tag = " 🆕" if is_novel else ""
        esc_tag = " ⚠ ESCALATE" if escalate else ""

        print(f"  Category:    {cat}")
        print(f"  Confidence:  {conf:.4f} ({conf:.1%})")
        print(f"  Method:      {method}{novel_tag}{esc_tag}")
        if llm_rationale:
            print(f"  LLM Judge:   {llm_rationale}")

        # Check expectation
        match = method == s["expect_method"]
        status = "✅ PASS" if match else f"❌ FAIL (expected {s['expect_method']})"
        print(f"  Result:      {status}")

        results.append({
            "scenario": s["name"],
            "expected": s["expect_method"],
            "actual": method,
            "pass": match,
        })

    # Summary
    passed = sum(1 for r in results if r["pass"])
    total = len(results)
    print(f"\n{'=' * 70}")
    print(f"  SUMMARY: {passed}/{total} scenarios matched expected cascade path")
    if passed == total:
        print("  ✅ All cascade paths working correctly.")
    else:
        print("  ⚠ Some paths did not match expectations. Review above.")
        for r in results:
            if not r["pass"]:
                print(f"    MISS: {r['scenario']} → got {r['actual']}, expected {r['expected']}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    run_cascade_tests()
