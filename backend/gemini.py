import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_code(language, code):

    prompt = f"""
You are a senior software engineer.

Analyze the following {language} code.

Return ONLY valid JSON.

Do not write explanations.
Do not use markdown.
Do not wrap the JSON inside ```.

Return exactly this schema:

{{
    "level":"",
    "score":0,
    "time_complexity":"",
    "space_complexity":"",
    "strengths":[],
    "weaknesses":[],
    "interview_question":""
}}
Scoring Guidelines:

100 = Production-quality code
90-99 = Excellent, interview-ready
80-89 = Good solution with minor improvements
70-79 = Correct but needs improvement
60-69 = Basic understanding
Below 60 = Major issues or incorrect solution

Be strict but fair.

Code:

{code}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown fences if present
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:

        return {
            "level": "Unknown",
            "score": 0,
            "time_complexity": "Unknown",
            "space_complexity": "Unknown",
            "strengths": [],
            "weaknesses": [
                "Gemini returned an invalid JSON response."
            ],
            "interview_question": "No question generated."
        }