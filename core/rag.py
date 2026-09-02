"""
Learning Engines (RAG) - Retrieves courses for skill gaps and generates quizzes from materials.
Uses direct REST calls to Ollama to avoid Langchain hanging issues.
"""
import os
import sys
import json
import requests
from typing import Dict, Any, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.embeddings import get_chroma_collection, get_embedding_model


def _call_llm(prompt: str) -> str:
    """Call Groq or Ollama via REST API directly to avoid LangChain timeouts/hanging."""
    try:
        if config.USE_GROQ and config.GROQ_API_KEY:
            print(f"  [LLM] Calling Groq model: {config.GROQ_MODEL}...")
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {config.GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": config.GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens": 1000,
                },
                timeout=15,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print(f"  [LLM] Calling Ollama model: {config.OLLAMA_MODEL}...")
            url = f"{config.OLLAMA_BASE_URL}/api/chat"
            payload = {
                "model": config.OLLAMA_MODEL,
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
    except Exception as e:
        return f"Error connecting to LLM: {str(e)}"


class CourseRecommender:
    """Retrieves relevant iGOT courses based on identified skill gaps."""
    
    def __init__(self):
        self.collection = get_chroma_collection() # Note: To be pointed to 'courses' later
        self.embedding_model = get_embedding_model()
    
    def suggest_courses(self, skill_gaps: List[str], k: int = 3) -> Dict[str, Any]:
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


class QuizGenerator:
    """Generates MCQs from uploaded learning materials."""
    
    def generate_mcqs(self, document_text: str, num_questions: int = 5) -> Dict[str, Any]:
        """
        Generate multiple choice questions based on the provided text.
        """
        # Truncate text if too long for prompt to avoid context window issues
        safe_text = document_text[:5000]
        
        prompt = f"""You are an AI Assessment Engine for MoSPI.
Generate {num_questions} Multiple Choice Questions (MCQs) based ONLY on the following learning material.

## Learning Material:
{safe_text}

## Instructions:
1. Generate exactly {num_questions} questions.
2. Each question must have 4 options (A, B, C, D) and 1 correct answer.
3. Provide a brief explanation for the correct answer.
4. Output MUST be ONLY valid JSON matching this exact structure:
{{
  "quiz": [
    {{
      "question": "The question text?",
      "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
      "correct_answer": "Option A text",
      "explanation": "Brief explanation of why it is correct."
    }}
  ]
}}
DO NOT include any markdown formatting like ```json. Return ONLY the raw JSON object.
"""

        raw_output = _call_llm(prompt)
        
        # Attempt to parse the JSON
        try:
            clean = raw_output.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            parsed_quiz = json.loads(clean)
            return {"status": "success", "data": parsed_quiz}
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Failed to parse LLM output as JSON. Error: {str(e)}",
                "raw_output": raw_output
            }


# --- CLI Test ---
if __name__ == "__main__":
    print("Initializing Learning Engines...")
    recommender = CourseRecommender()
    quiz_gen = QuizGenerator()
    
    print(f"\n=============================================")
    print(f"Testing CourseRecommender:")
    gaps = ["Data Visualization with Python", "Advanced SQL"]
    rec_result = recommender.suggest_courses(gaps)
    print("\nPathway:")
    print(rec_result["suggested_pathway"])
    
    print(f"\n=============================================")
    print(f"Testing QuizGenerator:")
    sample_text = "The Ministry of Statistics and Programme Implementation (MoSPI) is a ministry of Government of India concerned with coverage and quality aspects of statistics released. The surveys conducted by the Ministry are based on scientific sampling methods."
    quiz_result = quiz_gen.generate_mcqs(sample_text, num_questions=2)
    print("\nGenerated Quiz (JSON):")
    print(json.dumps(quiz_result, indent=2))
    print(f"=============================================\n")
