"""
Agentic Layer v4.0 — LMS Decoupled Architecture

Three specialized agents form the decision pipeline for capacity building:
  1. ProfileAgent:      Uses CompetencyAnalyzer to extract skills & gaps from raw input.
  2. PathwayAgent:      Uses CourseRecommender to build a personalized learning journey.
  3. AssessmentAgent:   Uses QuizGenerator to build assessments from uploaded materials.

Each agent returns an AgentResult dict.
"""
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.classifier import CompetencyAnalyzer
from core.rag import CourseRecommender, QuizGenerator


# ──────────────────────────────────────────────────────────────
# Agent 1: ProfileAgent 
# ──────────────────────────────────────────────────────────────
class ProfileAgent:
    """
    Accepts raw user data and produces a structured competency profile.
    """

    def __init__(self):
        self.analyzer = CompetencyAnalyzer()

    def run(self, user_data: dict) -> dict:
        """Execute profiling logic and return skill gaps."""
        designation = user_data.get("designation", "Unknown Official")
        profile_text = user_data.get("profile_text", "")
        
        # Call the Competency Analyzer
        analysis = self.analyzer.analyze_profile(designation, profile_text)
        
        if not analysis:
            return {
                "success": False,
                "current_skills": [],
                "skill_gaps": [],
                "analysis_summary": "Failed to analyze profile."
            }
            
        return {
            "success": True,
            "current_skills": analysis.get("current_skills", []),
            "skill_gaps": analysis.get("skill_gaps", []),
            "analysis_summary": analysis.get("analysis_summary", "")
        }


# ──────────────────────────────────────────────────────────────
# Agent 2: PathwayAgent
# ──────────────────────────────────────────────────────────────
class PathwayAgent:
    """
    Accepts skill gaps and generates a personalized learning pathway 
    with recommended iGOT courses.
    """

    def __init__(self):
        self.recommender = CourseRecommender()

    def run(self, skill_gaps: list) -> dict:
        """Generate learning pathway."""
        if not skill_gaps:
            return {
                "pathway": "No skill gaps identified. Keep up the good work!",
                "courses": []
            }
            
        result = self.recommender.suggest_courses(skill_gaps)
        
        return {
            "pathway": result.get("suggested_pathway", ""),
            "courses": result.get("courses", [])
        }


# ──────────────────────────────────────────────────────────────
# Agent 3: AssessmentAgent
# ──────────────────────────────────────────────────────────────
class AssessmentAgent:
    """
    Handles the generation of quizzes from learning materials.
    """

    def __init__(self):
        self.quiz_gen = QuizGenerator()

    def run(self, document_text: str, num_questions: int = 5) -> dict:
        """Generate MCQs from document text."""
        result = self.quiz_gen.generate_mcqs(document_text, num_questions)
        return result


# ──────────────────────────────────────────────────────────────
# Main Orchestrator (LMSLayer)
# ──────────────────────────────────────────────────────────────
class LMSLayer:
    """
    Thin orchestrator that wraps the three specialized agents.
    """

    def __init__(self):
        self.profiler = ProfileAgent()
        self.pathway = PathwayAgent()
        self.assessment = AssessmentAgent()

    def generate_learning_plan(self, designation: str, profile_text: str) -> dict:
        """
        End-to-end flow: Profile -> Gaps -> Pathway
        """
        # 1. Profile the user
        profile_result = self.profiler.run({
            "designation": designation,
            "profile_text": profile_text
        })
        
        if not profile_result["success"]:
            return {"error": "Failed to generate profile."}
            
        # 2. Generate Pathway based on gaps
        pathway_result = self.pathway.run(profile_result["skill_gaps"])
        
        return {
            "profile": profile_result,
            "learning_plan": pathway_result
        }


# ──────────────────────────────────────────────────────────────
# CLI Test
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("  LMS Agentic Layer v4.0 — Self-Test")
    print("=" * 70)

    lms = LMSLayer()
    
    test_designation = "Data Entry Operator"
    test_profile = "I have been doing manual data entry for 3 years. I want to learn data analysis but don't know Python or SQL."
    
    print(f"\nRunning Learning Plan Generator for: {test_designation}")
    plan = lms.generate_learning_plan(test_designation, test_profile)
    
    print("\n[Profile Analysis]")
    print(json.dumps(plan.get("profile"), indent=2))
    
    print("\n[Learning Pathway]")
    print(plan.get("learning_plan", {}).get("pathway", ""))
    
    print("\n" + "=" * 70)
    print("  All agent self-tests complete.")
    print("=" * 70)
