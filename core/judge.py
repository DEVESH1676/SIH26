"""
LLM-as-Judge Evaluation Framework
Evaluates learner's subjective answers to assessment questions on a 3-axis rubric:
  - Accuracy (1-5): Is the answer factually correct?
  - Comprehension (1-5): Does the user understand the core concept?
  - Completeness (1-5): Did they address all parts of the question?
"""
import os
import sys
import json
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class SubjectiveAssessor:
    """
    Evaluates learner answers using LLM-as-Judge pattern.
    """

    PASSING_SCORE = 3.5  # Average score required to "pass"

    def evaluate_answer(self, question: str, expected_key_points: str, learner_answer: str) -> dict:
        """Evaluate a learner's subjective answer."""

        prompt = f"""You are a Senior Assessor for the Ministry of Statistics (MoSPI). 
Evaluate the learner's answer to the following assessment question.

## Assessment Context:
- Question: {question}
- Expected Key Points: {expected_key_points}

## Learner's Answer:
{learner_answer}

## Evaluation Rubric:
Score each axis from 1 (worst) to 5 (best):
1. **Accuracy**: Is the answer factually correct? 
2. **Comprehension**: Does the learner demonstrate a clear understanding of the core concept?
3. **Completeness**: Did the learner address all the expected key points?

## Response Format:
Return ONLY valid JSON (no markdown fences, no explanation outside JSON):
{{"accuracy": <1-5>, "comprehension": <1-5>, "completeness": <1-5>, "feedback": "<one short paragraph of constructive feedback directly addressing the learner>"}}
"""
        raw_result = self._call_judge_llm(prompt)
        return self._parse_result(raw_result)

    def _call_judge_llm(self, prompt: str) -> str:
        """Call Groq/Ollama for evaluation."""
        try:
            if config.GROQ_API_KEY:
                resp = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {config.GROQ_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": config.GROQ_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.1,
                        "max_tokens": 300,
                    },
                    timeout=15,
                )
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"].strip()
            else:
                resp = requests.post(
                    f"{config.OLLAMA_BASE_URL}/api/chat",
                    json={
                        "model": config.OLLAMA_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": False,
                        "options": {"temperature": 0.1},
                    },
                    timeout=5,
                )
                if resp.status_code == 200:
                    return resp.json().get("message", {}).get("content", "").strip()
                return f"Error: Ollama returned HTTP {resp.status_code}"
        except Exception as e:
            return f"LLM judge call failed: {str(e)}"

    def _parse_result(self, raw: str) -> dict:
        """Parse LLM response into structured JudgeResult."""
        fallback = {
            "accuracy": 3,
            "comprehension": 3,
            "completeness": 3,
            "feedback": f"Evaluation failed to parse. Raw: {raw[:150]}",
        }

        try:
            clean = raw.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            parsed = json.loads(clean)

            scores = {}
            for axis in ["accuracy", "comprehension", "completeness"]:
                val = parsed.get(axis, 3)
                scores[axis] = max(1, min(5, int(val)))

            scores["feedback"] = parsed.get("feedback", "No feedback provided.")
        except (json.JSONDecodeError, Exception):
            scores = fallback

        # Calculate overall score
        overall = sum(scores[a] for a in ["accuracy", "comprehension", "completeness"]) / 3.0
        scores["overall"] = round(overall, 2)
        scores["passed"] = scores["overall"] >= self.PASSING_SCORE

        return scores


# ──────────────────────────────────────────────────────────────
# CLI Test
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("  SubjectiveAssessor — Self-Test")
    print("=" * 70)

    judge = SubjectiveAssessor()

    # Test 1: Good Answer
    print("\n── Test 1: Good Answer ──")
    r1 = judge.evaluate_answer(
        question="What is the primary difference between a census and a sample survey?",
        expected_key_points="Census covers the entire population. Sample survey covers a representative subset to infer about population.",
        learner_answer="A census tries to count every single person or item in a population. A sample survey only looks at a smaller, representative group to make estimates about the whole population, which is usually cheaper and faster."
    )
    print(f"  Scores: Acc={r1['accuracy']} Comp={r1['comprehension']} Cmpl={r1['completeness']}")
    print(f"  Overall: {r1['overall']}, Passed: {r1['passed']}")
    print(f"  Feedback: {r1['feedback']}")

    # Test 2: Poor Answer
    print("\n── Test 2: Poor Answer ──")
    r2 = judge.evaluate_answer(
        question="What is the primary difference between a census and a sample survey?",
        expected_key_points="Census covers the entire population. Sample survey covers a representative subset to infer about population.",
        learner_answer="A census is done by the government. A survey is done by companies online."
    )
    print(f"  Scores: Acc={r2['accuracy']} Comp={r2['comprehension']} Cmpl={r2['completeness']}")
    print(f"  Overall: {r2['overall']}, Passed: {r2['passed']}")
    print(f"  Feedback: {r2['feedback']}")

    print("\n" + "=" * 70)
    print("  Self-test complete.")
    print("=" * 70)
