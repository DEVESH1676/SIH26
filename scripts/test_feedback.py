import os
import sys

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.feedback import FeedbackStore

def main():
    store = FeedbackStore(db_path="/home/devesh/Hackathon/data/feedback.db")
    print("Store initialized.")

    store.log_run(
        ticket_id="TICKET-UAT-001",
        category="Network",
        confidence=0.88,
        resolution_steps="Step 1\nStep 2",
        judge_scores={"safety": 5, "accuracy": 4},
        agent_action="Escalate",
        human_override='{"new_category": "Hardware"}',
        outcome="Resolved"
    )
    print("Logged resolution successfully.")

if __name__ == "__main__":
    main()
