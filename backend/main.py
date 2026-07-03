import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.models import CodeRequest
from backend.gemini import (
    analyze_code,
    generate_interview_questions,
    evaluate_interview_answers,
    review_code
)
from backend.history import save_history

APP_VERSION = "v1.5.0"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="What's My Level? API",
    description="Backend API for the AI-powered coding assessment platform.",
    version="1.5.0"
)


class ReviewRequest(BaseModel):
    language: str
    code: str


class EvaluateInterviewRequest(BaseModel):
    language: str
    code: str
    questions: list[str]
    answers: list[str]


@app.get("/")
def home():
    return {
        "message": "🚀 Welcome to What's My Level API!",
        "status": "Backend is running successfully."
    }


@app.get("/about")
def about():
    return {
        "project": "What's My Level?",
        "version": "1.5.0",
        "developer": "Pragadhishwar A"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
def analyze(request: CodeRequest):
    try:
        result = analyze_code(
            request.language,
            request.code
        )

        save_history(result, request.language)

        return result

    except Exception as e:
        logger.error("Backend error in /analyze: %r", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/interview")
def interview(request: CodeRequest):
    return generate_interview_questions(
        request.language,
        request.code
    )


@app.post("/evaluate-interview")
def evaluate_interview(request: EvaluateInterviewRequest):
    try:
        return evaluate_interview_answers(
            request.language,
            request.code,
            request.questions,
            request.answers
        )
    except Exception as e:
        logger.error("Backend error in /evaluate-interview: %r", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/review-code")
def review(request: ReviewRequest):
    return review_code(
        request.language,
        request.code
    )