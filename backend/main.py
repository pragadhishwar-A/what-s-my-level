import logging
from fastapi import FastAPI, HTTPException
from backend.models import CodeRequest
from backend.gemini import analyze_code
from backend.history import save_history

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


from fastapi import HTTPException

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
        print("========== BACKEND ERROR ==========")
        print(repr(e))
        print("===================================")

        raise HTTPException(status_code=500, detail=str(e))