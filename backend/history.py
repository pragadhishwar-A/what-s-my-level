import json
import os
from datetime import datetime

FILE_NAME = "history.json"


def load_history():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_history(result, language):
    history = load_history()

    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "language": language,
        "level": result["level"],
        "score": result["score"],
        "time_complexity": result["time_complexity"],
        "space_complexity": result["space_complexity"]
    })

    with open(FILE_NAME, "w") as f:
        json.dump(history, f, indent=4)