"""
Learning Engines (RAG) - Retrieves courses for skill gaps and generates quizzes from materials.
Uses direct REST calls to Ollama to avoid Langchain hanging issues.
"""
import os
import sys
from typing import Any

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import get_settings

settings = get_settings()
from core.embeddings import get_chroma_collection, get_embedding_model


def _call_llm(prompt: str) -> str:
    """Call Groq or Ollama via REST API directly to avoid LangChain timeouts/hanging."""
    try:
        if settings.use_groq and settings.groq_api_key:
            print(f"  [LLM] Calling Groq model: {settings.groq_model}...")
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.groq_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens": 1000,
                },
                timeout=15,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print(f"  [LLM] Calling Ollama model: {settings.ollama_model}...")
            url = f"{settings.ollama_base_url}/api/chat"
            payload = {
                "model": settings.ollama_model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": 0.2}
            }
            response = requests.post(url, json=payload, timeout=20)
            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', "Error: No content returned").strip()
            else:
                return f"Error: Ollama API returned HTTP {response.status_code}\n{response.text}"
    except Exception as e:  # noqa: BLE001
        return f"Error connecting to LLM: {e!s}"


class CourseRecommender:
    """Retrieves relevant iGOT courses based on identified skill gaps."""
    
    def __init__(self):
        self.collection = get_chroma_collection() # Note: To be pointed to 'courses' later
        self.embedding_model = get_embedding_model()
    
    def suggest_courses(self, skill_gaps: list[str], k: int = 3) -> dict[str, Any]:
        """
        Retrieve K most relevant courses for the given skill gaps.
        """
        query_text = " ".join(skill_gaps)
        if not query_text:
            return {"suggested_pathway": "No skill gaps identified.", "courses": []}

        query_embedding = self.embedding_model.encode(query_text).tolist()
        
        # Retrieve courses from ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        
        retrieved_courses = []
        course_context_parts = []
        if results['ids'] and results['ids'][0]:
            for i, (doc, meta, dist) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                similarity = 1.0 - dist
                course_id = meta.get("course_id", results['ids'][0][i])
                course_name = meta.get("course_name", f"Course {course_id}")
                
                retrieved_courses.append({
                    "id": course_id,
                    "name": course_name,
                    "similarity": similarity,
                    "document": doc
                })
                
                course_context_parts.append(
                    f"Course {i+1}: {course_name}\nDescription/Skills: {doc}\n"
                )
        
        course_context = "\n".join(course_context_parts) if course_context_parts else "No relevant courses found in the catalog."
        
        prompt = f"""You are an AI Learning Advisor for MoSPI.
Based on the official's identified skill gaps and the available iGOT/NSSTA courses, suggest a personalized Learning Pathway.
You must execute a hybrid recommendation strategy:
- Micro-learning / On-demand: Asynchronous iGOT karmayogi courses.
- Institutional / Physical / Cohort-based: NSSTA TPAC calendar schedules (workshop dates, eligibility by cadre).

## Identified Skill Gaps:
{", ".join(skill_gaps)}

## Available Courses & Training Calendar (from iGOT & NSSTA):
{course_context}

## Instructions:
1. Recommend the most relevant hybrid mix of courses from the list above to address the skill gaps.
2. Explain WHY each course/workshop is recommended.
3. Be encouraging and format the output as a clean, actionable learning pathway.
"""

        pathway_text = _call_llm(prompt)
        
        return {
            "suggested_pathway": pathway_text,
            "courses": retrieved_courses
        }





# --- CLI Test ---
if __name__ == "__main__":
    print("Initializing Learning Engines...")
    recommender = CourseRecommender()
    
    print("\n=============================================")
    print("Testing CourseRecommender:")
    gaps = ["Data Visualization with Python", "Advanced SQL"]
    rec_result = recommender.suggest_courses(gaps)
    print("\nPathway:")
    print(rec_result["suggested_pathway"])
    print("=============================================\n")
