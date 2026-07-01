import os
import json
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError
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

Level must be one of: "Beginner", "Intermediate", "Advanced", "Expert"

Scoring Guidelines:
100   = Production-quality code
90-99 = Excellent, interview-ready
80-89 = Good solution with minor improvements
70-79 = Correct but needs improvement
60-69 = Basic understanding
Below 60 = Major issues or incorrect solution

Keep every answer concise.
Provide at most 3 optimization suggestions.
Each suggestion should be one short sentence.
Be strict but fair.

Code:
{code}
"""

    try:
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    except Exception as e:
        print("Gemini Error:", e)
        raise e

    text = response.text.strip()

    # Strip markdown fences if Gemini adds them despite instructions
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(text)

        # Validate required keys exist
        required_keys = [
            "level", "score", "time_complexity", "space_complexity",
            "strengths", "weaknesses", "optimization_suggestions", "interview_question"
        ]
        for key in required_keys:
            if key not in result:
                raise ValueError(f"Missing key in response: {key}")

        # Clamp score to 0-100
        result["score"] = max(0, min(100, int(result["score"])))

        return result

    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Gemini response parse failed: {e}\nRaw response: {text}")
        raise ValueError(f"Failed to parse Gemini response: {e}")
 

    except ClientError as e:
        if "429" in str(e):
            raise HTTPException(status_code=429, detail="Gemini quota exceeded. Try again later.")
            raise HTTPException(status_code=500, detail=str(e))