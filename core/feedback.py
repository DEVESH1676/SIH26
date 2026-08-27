"""
Feedback Store - Captures every pipeline run for learning loop and audit trail.

Stores classification results, resolution steps, LLM-as-Judge scores,
agent decisions, and human overrides in a local SQLite database.
"""
import os
import sys
import json
import sqlite3
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FeedbackStore:
    """Persistent SQLite store for pipeline run feedback and resolution tracking."""

    def __init__(self, db_path=None):
        if db_path is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(project_root, "data", "feedback.db")

        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        """Create the resolutions table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS resolutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT,
                category TEXT,
                confidence REAL,
                resolution_steps TEXT,
                judge_scores TEXT,
                agent_action TEXT,
                human_override TEXT,
                outcome TEXT,
                created_at TIMESTAMP
            )
        """)
        self.conn.commit()

    def log_run(
        self,
        ticket_id: str,
        category: str,
        confidence: float,
        resolution_steps: str = None,
        judge_scores: dict = None,
        agent_action: str = None,
        human_override: str = None,
        outcome: str = None,
    ):
        """
        Log a single pipeline run to the feedback table.

        Args:
            ticket_id: Unique ticket identifier
            category: Predicted category
            confidence: Classifier confidence score (0.0 - 1.0)
            resolution_steps: Generated resolution text
            judge_scores: Dict with keys correctness, completeness, safety, clarity, overall, critique
            agent_action: Which agent acted and what it decided
            human_override: Non-null if a human corrected the agent's decision
            outcome: Final outcome — "resolved", "reopened", "escalated"
        """
        scores_json = json.dumps(judge_scores) if isinstance(judge_scores, dict) else judge_scores
        now = datetime.now(timezone.utc).isoformat()

        self.conn.execute(
            """
            INSERT INTO resolutions
                (ticket_id, category, confidence, resolution_steps,
                 judge_scores, agent_action, human_override, outcome, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (ticket_id, category, confidence, resolution_steps,
             scores_json, agent_action, human_override, outcome, now),
        )
        self.conn.commit()

    def get_all(self) -> list[dict]:
        """Return all rows as a list of dicts."""
        cursor = self.conn.execute("SELECT * FROM resolutions ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

    def get_by_category(self, category: str) -> list[dict]:
        """Return rows filtered by category."""
        cursor = self.conn.execute(
            "SELECT * FROM resolutions WHERE category = ? ORDER BY created_at DESC",
            (category,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def count(self) -> int:
        """Return total number of logged runs."""
        cursor = self.conn.execute("SELECT COUNT(*) FROM resolutions")
        return cursor.fetchone()[0]

    def close(self):
        """Close the database connection."""
        self.conn.close()


# --- CLI Self-Test ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Feedback Store — Self Test")
    print("=" * 60)

    store = FeedbackStore()
    print(f"\n✓ Database created at: {store.db_path}")

    # Insert a test row
    store.log_run(
        ticket_id="TEST-001",
        category="Infrastructure",
        confidence=0.92,
        resolution_steps="1. Check server status\n2. Restart service\n3. Verify connectivity",
        judge_scores={
            "correctness": 5,
            "completeness": 4,
            "safety": 5,
            "clarity": 4,
            "overall": 4.5,
            "critique": "Good resolution, minor clarity improvements possible.",
        },
        agent_action="TriageAgent: routed to Cloud Platform Engineering",
        human_override=None,
        outcome="resolved",
    )
    print("✓ Test row inserted successfully")

    # Query it back
    rows = store.get_all()
    print(f"✓ Total rows in feedback table: {len(rows)}")

    if rows:
        row = rows[0]
        print(f"\n  Sample row:")
        print(f"    ticket_id:    {row['ticket_id']}")
        print(f"    category:     {row['category']}")
        print(f"    confidence:   {row['confidence']}")
        print(f"    judge_scores: {row['judge_scores']}")
        print(f"    outcome:      {row['outcome']}")
        print(f"    created_at:   {row['created_at']}")

    store.close()
    print("\n✓ Feedback store self-test PASSED")
