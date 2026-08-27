"""
Confidence Calibration Check — Phase 1 (CALIB-01)

Validates whether the classifier's confidence bands actually correlate with
prediction accuracy. Groups all 150 existing tickets by their confidence score
into three bands and measures accuracy per band.

Expected outcome:
  - High band (>0.75): should be ≥80% accurate
  - Medium band (0.40–0.75): intermediate accuracy
  - Low band (<0.40): expected low accuracy (these get escalated)

If the high band is <80% accurate, the cascade thresholds need recalibration
before building v3 features.
"""
import os
import sys

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.classifier import TicketClassifier
from core.embeddings import get_chroma_collection


def run_calibration():
    print("=" * 70)
    print("  CONFIDENCE CALIBRATION CHECK")
    print("  Validating classifier thresholds against stored tickets")
    print("=" * 70)

    # Initialize classifier (builds centroids)
    clf = TicketClassifier()

    # Fetch all stored tickets with their ground-truth metadata
    collection = get_chroma_collection()
    all_data = collection.get(include=["documents", "metadatas"])

    total_tickets = len(all_data["ids"])
    print(f"\n📊 Total tickets in ChromaDB: {total_tickets}")

    if total_tickets == 0:
        print("⚠ No tickets found. Run embeddings.py first.")
        return

    # --- Classify each ticket and bucket by confidence band ---
    bands = {
        "high (>0.75)": {"correct": 0, "total": 0, "misses": []},
        "medium (0.40-0.75)": {"correct": 0, "total": 0, "misses": []},
        "low (<0.40)": {"correct": 0, "total": 0, "misses": []},
    }

    # Track per-category accuracy
    category_stats = {}
    overall_correct = 0

    for idx, (doc, meta, ticket_id) in enumerate(
        zip(all_data["documents"], all_data["metadatas"], all_data["ids"])
    ):
        true_category = meta.get("category", "Unknown")
        result = clf.classify(title="", description=doc)

        predicted = result["category"]
        confidence = result["confidence"]
        is_correct = predicted == true_category

        if is_correct:
            overall_correct += 1

        # Determine band
        if confidence > 0.75:
            band_key = "high (>0.75)"
        elif confidence >= 0.40:
            band_key = "medium (0.40-0.75)"
        else:
            band_key = "low (<0.40)"

        bands[band_key]["total"] += 1
        if is_correct:
            bands[band_key]["correct"] += 1
        else:
            bands[band_key]["misses"].append({
                "ticket_id": ticket_id,
                "true": true_category,
                "predicted": predicted,
                "confidence": round(confidence, 4),
            })

        # Per-category stats
        if true_category not in category_stats:
            category_stats[true_category] = {"correct": 0, "total": 0}
        category_stats[true_category]["total"] += 1
        if is_correct:
            category_stats[true_category]["correct"] += 1

        # Progress indicator
        if (idx + 1) % 25 == 0:
            print(f"  Processed {idx + 1}/{total_tickets} tickets...")

    # --- Report ---
    print(f"\n{'=' * 70}")
    print("  CALIBRATION RESULTS")
    print(f"{'=' * 70}")
    print(f"\n  Overall accuracy: {overall_correct}/{total_tickets} = {overall_correct/total_tickets:.1%}")

    print(f"\n  {'Band':<25} {'Correct':>8} {'Total':>8} {'Accuracy':>10}")
    print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*10}")

    calibrated = True
    for band_name, data in bands.items():
        if data["total"] > 0:
            acc = data["correct"] / data["total"]
            marker = "✓" if (band_name.startswith("high") and acc >= 0.80) else ""
            if band_name.startswith("high") and acc < 0.80:
                marker = "⚠ UNCALIBRATED"
                calibrated = False
            print(f"  {band_name:<25} {data['correct']:>8} {data['total']:>8} {acc:>9.1%} {marker}")
        else:
            print(f"  {band_name:<25} {'—':>8} {0:>8} {'N/A':>10}")

    # Per-category breakdown
    print(f"\n  {'Category':<25} {'Correct':>8} {'Total':>8} {'Accuracy':>10}")
    print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*10}")
    for cat, stats in sorted(category_stats.items()):
        acc = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
        print(f"  {cat:<25} {stats['correct']:>8} {stats['total']:>8} {acc:>9.1%}")

    # Show misclassifications in high-confidence band (most concerning)
    high_misses = bands["high (>0.75)"]["misses"]
    if high_misses:
        print(f"\n  ⚠ High-confidence misclassifications ({len(high_misses)}):")
        for miss in high_misses[:10]:
            print(f"    {miss['ticket_id']}: {miss['true']} → {miss['predicted']} (conf: {miss['confidence']})")

    # --- Verdict ---
    print(f"\n{'=' * 70}")
    if calibrated:
        print("  ✅ CALIBRATION PASSED — High-confidence band ≥80% accurate.")
        print("     Cascade thresholds (0.75 / 0.40) are valid for v3.")
    else:
        print("  ❌ CALIBRATION FAILED — High-confidence band <80% accurate.")
        print("     Thresholds need adjustment before building cascade classifier.")
        print("     Consider: lower the high threshold or apply temperature scaling.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    run_calibration()
