from fastapi import FastAPI
from backend.models import CodeRequest
from backend.gemini import analyze_code

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

    result = analyze_code(
        request.language,
        request.code
    )

    return result