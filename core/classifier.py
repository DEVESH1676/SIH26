"""
Competency Analyzer — Skill Gap Analysis Engine
Analyzes a user's profile to identify current competencies and missing skill gaps
against the MoSPI competency framework.
"""
import os
import sys
import json
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class CompetencyAnalyzer:
    """Analyzes user profiles to identify skill gaps."""

    def __init__(self):
        # We can integrate ChromaDB later if we want to match against a DB of competencies
        pass

    def _call_llm(self, prompt: str) -> dict | None:
        """Call LLM (Groq/Ollama) to perform the competency extraction."""
        try:
            if config.USE_GROQ and config.GROQ_API_KEY:
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
                        "max_tokens": 500,
                    },
                    timeout=15,
                )
                resp.raise_for_status()
                content = resp.json()["choices"][0]["message"]["content"].strip()
            else:
                resp = requests.post(
                    f"{config.OLLAMA_BASE_URL}/api/generate",
                    json={
                        "model": config.OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json",
                    },
                    timeout=10,
                )
                resp.raise_for_status()
                content = resp.json()["response"].strip()
                
            # Strip markdown fences if present
            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(content)
            
        except Exception as e:
            print(f"  ⚠ LLM analysis failed: {e}")
            return None

    def analyze_profile(self, designation: str, profile_text: str) -> dict:
        """
        Analyze the official's profile and return their current skills and identified gaps.
        """
        prompt = f"""You are an HR Capacity Building AI for the Ministry of Statistics (MoSPI).
Analyze this official's profile against the FRAC (Framework for Roles, Activities, and Competencies) model.
Identify their current competencies and explicitly list their missing 'Skill Gaps' based on standard requirements for their designation.

Designation: {designation}
Profile/Experience: {profile_text}

Domains to map:
1. Domain (Statistical Competencies)
2. Functional (Functional & Digital Competencies)
3. Behavioral (Behavioral Competencies)

Reply ONLY with valid JSON (no markdown) in the following format:
{{
  "current_skills": {{"Domain": [], "Functional": [], "Behavioral": []}},
  "skill_gaps": {{"Domain": [], "Functional": [], "Behavioral": []}},
  "analysis_summary": "A 2-sentence summary of their competency profile."
}}
"""
        result = self._call_llm(prompt)
        
        if not result:
            # Fallback
            return {
                "current_skills": {"Domain": ["General Administration"], "Functional": [], "Behavioral": []},
                "skill_gaps": {"Domain": ["Data Analysis"], "Functional": ["Digital Governance"], "Behavioral": []},
                "analysis_summary": "Could not perform deep analysis. Assuming default gaps for capacity building."
            }
            
        return result


# --- CLI Test ---
if __name__ == "__main__":
    print("Initializing Competency Analyzer...")
    analyzer = CompetencyAnalyzer()
    
    print("\nTesting with Sample Profile...")
    sample_designation = "Statistical Officer"
    sample_profile = "Worked on field data collection for 5 years. Proficient in MS Excel and basic data entry. No experience with modern data pipelines or Python."
    
    result = analyzer.analyze_profile(sample_designation, sample_profile)
    print(json.dumps(result, indent=2))
