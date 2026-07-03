import os
import json
import logging
from dotenv import load_dotenv
from google import genai

load_dotenv()

logger = logging.getLogger(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_code(language: str, code: str) -> dict:

    prompt = f"""
You are a senior software engineer.

Analyze the following {language} code.

Return ONLY valid JSON.

Do not write explanations.
Do not use markdown.
Do not wrap the JSON inside ```.

Return exactly this schema:

{{
    "level": "",
    "score": 0,
    "time_complexity": "",
    "space_complexity": "",
    "strengths": [],
    "weaknesses": [],
    "optimization_suggestions": [],
    "interview_question": ""
}}

Level must be one of:
Beginner
Intermediate
Advanced
Expert

Scoring Guidelines:

100 = Production-quality code
90-99 = Excellent, interview-ready
80-89 = Good solution with minor improvements
70-79 = Correct but needs improvement
60-69 = Basic understanding
Below 60 = Major issues or incorrect solution

Keep every answer concise.
Provide at most 3 optimization suggestions.
Each suggestion should be one short sentence.

Code:

{code}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        result = json.loads(text)

        required_keys = [
            "level",
            "score",
            "time_complexity",
            "space_complexity",
            "strengths",
            "weaknesses",
            "optimization_suggestions",
            "interview_question"
        ]

        for key in required_keys:
            if key not in result:
                raise ValueError(f"Missing key: {key}")

        result["score"] = max(0, min(100, int(result["score"])))

        return result

    except Exception as e:
        logger.error(f"Gemini Error: {e}")

        return {
            "level": "Unknown",
            "score": 0,
            "time_complexity": "Unknown",
            "space_complexity": "Unknown",
            "strengths": [],
            "weaknesses": [
                "Failed to analyze code."
            ],
            "optimization_suggestions": [],
            "interview_question": "No interview question generated."
        }


def generate_interview_questions(language: str, code: str):

    prompt = f"""
You are a Senior Software Engineer conducting a coding interview.

Based on the following {language} code, generate exactly 3 interview questions.

Rules:
- Keep each question under 25 words.
- Questions should test understanding, not ask for code.
- Cover:
  1. Logic
  2. Time/Space Complexity
  3. Optimization or edge cases

Return ONLY valid JSON.

{{
  "questions": [
    "",
    "",
    ""
  ]
}}

Code:
{code}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
     print("\n========== INTERVIEW ERROR ==========")
     print(repr(e))
     print("=====================================\n")
     raise
def evaluate_interview_answers(language, code, questions, answers):

    prompt = f"""
You are a Senior Software Engineer conducting a coding interview.

Evaluate the candidate's answers.

Programming Language:
{language}

Code:
{code}

Questions:
{questions}

Candidate Answers:
{answers}

Return ONLY valid JSON.

{{
    "overall_score": 0,
    "communication": 0,
    "technical_accuracy": 0,
    "problem_solving": 0,
    "feedback": [
        "",
        "",
        ""
    ],
    "recommendation": ""
}}

Rules:

overall_score : 0-10

communication : 0-10

technical_accuracy : 0-10

problem_solving : 0-10

feedback:
Maximum 3 short bullet points.

recommendation:
Either

Interview Ready

or

Needs More Practice

Return JSON only.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)
def review_code(language, code):

    prompt = f"""
You are a Senior Software Engineer.

Review the following {language} code line by line.

Return ONLY valid JSON.

Schema:

{{
  "line_reviews":[
    {{
      "line":1,
      "severity":"",
      "issue":"",
      "suggestion":""
    }}
  ]
}}

Rules:

Severity must be:

Low
Medium
High

Review at most 5 important lines.

Each issue must be one sentence.

Each suggestion must be one sentence.

Code:

{code}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)