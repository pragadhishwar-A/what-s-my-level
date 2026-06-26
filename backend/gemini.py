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
You are an expert software engineer.

Analyze the following {language} code.

Return ONLY valid JSON.

Do not explain anything.

Use this exact schema:

{{
    "level":"",
    "score":0,
    "time_complexity":"",
    "space_complexity":"",
    "strengths":[],
    "weaknesses":[],
    "interview_question":""
}}

Code:

{code}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown if Gemini wraps JSON in ```json
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)