from fastapi import FastAPI
from backend.models import CodeRequest

app = FastAPI(
    title="What's My Level? API",
    description="Backend API for the AI-powered coding assessment platform.",
    version="0.1.0"
)


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
        "version": "0.1.0",
        "developer": "Pragadhishwar A"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
def analyze(request: CodeRequest):

    score = 50 + min(len(request.code) // 10, 50)

    if score < 65:
        level = "Beginner"
    elif score < 85:
        level = "Intermediate"
    else:
        level = "Advanced"

    return {
        "level": level,
        "score": score,
        "language": request.language,
        "code_length": len(request.code),
        "time_complexity": "Coming Soon",
        "space_complexity": "Coming Soon",
        "feedback": "Gemini AI integration coming soon."
    }