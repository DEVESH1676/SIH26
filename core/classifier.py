"""
Competency Analyzer — Skill Gap Analysis Engine for MoSPI Officials.
Analyzes official profiles to identify current competencies and
missing skill gaps against the MoSPI competency framework.
"""
import os
import sys
import json
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings
from core.competency_framework import (
    COMPETENCY_FRAMEWORK,
    get_all_competency_ids,
    search_competencies,
)

settings = get_settings()


class CompetencyAnalyzer:
    """Analyzes user profiles to identify skill gaps against MoSPI framework."""

    def __init__(self):
        self.all_competency_ids = get_all_competency_ids()

    def _call_llm(self, prompt: str) -> dict | None:
        """Call LLM (Groq/Ollama) for competency analysis."""
        try:
            if settings.use_groq and settings.groq_api_key:
                resp = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.groq_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": settings.groq_model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.1,
                        "max_tokens": 1500,
                    },
                    timeout=30,
                )
                resp.raise_for_status()
                content = resp.json()["choices"][0]["message"]["content"].strip()
            else:
                resp = requests.post(
                    f"{settings.ollama_base_url}/api/generate",
                    json={
                        "model": settings.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json",
                    },
                    timeout=30,
                )
                resp.raise_for_status()
                content = resp.json()["response"].strip()

            # Strip markdown fences
            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(content)

        except Exception as e:
            print(f"  ⚠ LLM analysis failed: {e}")
            return None

    def analyze_profile(
        self,
        designation: str,
        profile_text: str,
        department: str = "",
        education: str = "",
        experience_years: int = 0,
        previous_trainings: list[str] = None,
    ) -> dict:
        """
        Analyze official's profile against MoSPI competency framework.
        
        Args:
            designation: Official's current designation
            profile_text: Summary of experience and duties
            department: Department/organization
            education: Educational qualifications
            experience_years: Years of experience
            previous_trainings: List of completed training titles
        """
        previous_trainings = previous_trainings or []
        
        # Get domain-specific competency lists for the prompt
        stat_comps = list(COMPETENCY_FRAMEWORK["statistical"].keys())
        tech_comps = list(COMPETENCY_FRAMEWORK["technical"].keys())
        dg_comps = list(COMPETENCY_FRAMEWORK["digital_governance"].keys())
        beh_comps = list(COMPETENCY_FRAMEWORK["behavioural"].keys())

        prompt = f"""You are an HR Capacity Building AI for the Ministry of Statistics and Programme Implementation (MoSPI), India.

Analyze this official's profile against the MoSPI Competency Framework for the Official Statistical System.

## Official Profile
- **Designation**: {designation}
- **Department**: {department or "Not specified"}
- **Education**: {education or "Not specified"}
- **Experience**: {experience_years} years
- **Previous Trainings**: {', '.join(previous_trainings) if previous_trainings else 'None recorded'}
- **Profile/Experience**: {profile_text}

## Competency Framework Domains

### Statistical Competencies
{', '.join(stat_comps)}

### Technical Competencies
{', '.join(tech_comps)}

### Digital Governance Competencies
{', '.join(dg_comps)}

### Behavioural Competencies
{', '.join(beh_comps)}

## Instructions
1. Assess the official's CURRENT competency level for each relevant domain.
2. Identify SPECIFIC skill gaps based on standard requirements for their designation.
3. Consider their experience level, education, and previous trainings.
4. Weight competencies based on relevance to their role.

Reply ONLY with valid JSON (no markdown fences):
{{
  "current_skills": [
    {{"id": "STAT-001", "name": "Survey Design", "level": "beginner|intermediate|advanced"}}
  ],
  "skill_gaps": [
    {{"id": "TECH-001", "name": "Python for Data Analysis", "priority": "high|medium|low", "reason": "Required for data processing in current role"}}
  ],
  "competency_summary": {{
    "statistical": "beginner|intermediate|advanced",
    "technical": "beginner|intermediate|advanced",
    "digital_governance": "beginner|intermediate|advanced",
    "behavioural": "beginner|intermediate|advanced"
  }},
  "analysis_summary": "2-sentence summary of their competency profile and key development needs."
}}
"""
        result = self._call_llm(prompt)

        if not result:
            # Conservative fallback
            return {
                "current_skills": [],
                "skill_gaps": [],
                "competency_summary": {
                    "statistical": "beginner",
                    "technical": "beginner",
                    "digital_governance": "beginner",
                    "behavioural": "beginner",
                },
                "analysis_summary": "Could not perform deep analysis. Recommend manual competency assessment.",
            }

        return result


# ── CLI Test ────────────────────────────────────────────────
if __name__ == "__main__":
    print("Initializing Competency Analyzer for MoSPI...")
    analyzer = CompetencyAnalyzer()

    result = analyzer.analyze_profile(
        designation="Statistical Officer",
        profile_text="Worked on field data collection for NSSO surveys for 5 years. Proficient in MS Excel and basic data entry. No experience with Python, SQL, or modern data analysis tools.",
        department="NSO",
        education="M.A. Statistics",
        experience_years=5,
        previous_trainings=["Basic Computer Training"],
    )
    print(json.dumps(result, indent=2))
