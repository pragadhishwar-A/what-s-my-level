import streamlit as st
import requests
import json
import os
from datetime import datetime
APP_VERSION="v1.4.0"

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="What's My Level?",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------
# Sidebar
# ---------------------------------
with st.sidebar:
    st.title("🚀 What's My Level?")
    st.write("AI-Powered Coding Assessment")
    st.divider()

    st.markdown("### Version")
    st.write(APP_VERSION)

    page = st.radio(
    "Navigation",
    [
        "🏠 Home",
        "📜 Analysis History",
        "🎤 Interview Coach",
        "📄 Code Mentor",
        "ℹ About"
    ]
)

    st.markdown("### Tech Stack")
    st.markdown("""
- Python
- Streamlit
- FastAPI
- Gemini 2.5 Flash
""")
    st.divider()
    st.info("Paste your code and get AI-powered feedback.")

# ---------------------------------
# Analysis History Page
# ---------------------------------
if page == "📜 Analysis History":
    st.title("📜 Analysis History")
elif page == "🎤 Interview Coach":

    st.title("🎤 AI Interview Coach")

    language = st.selectbox(
        "Programming Language",
        ["Python", "Java", "C++", "JavaScript"],
        key="interview_language"
    )

    code = st.text_area(
        "Paste your code",
        height=300,
        key="interview_code"
    )

    if st.button("🎯 Generate Interview Questions"):

        if not code.strip():
            st.warning("Please paste your code.")
        else:

            with st.spinner("Generating interview questions..."):

                try:

                    response = requests.post(
                    "http://127.0.0.1:8000/interview",
                    json={
                        "language": language,
                        "code": code
                    }
                )

                    if response.status_code == 200:

                        st.session_state["questions"] = response.json()["questions"]

                        st.success("Questions Generated!")

                    else:
                        st.error(response.text)

                except Exception as e:
                    st.error(e)


# -----------------------------
# Show Questions
# -----------------------------

if "questions" in st.session_state:

    answers = []

    for i, question in enumerate(st.session_state["questions"], start=1):

        st.subheader(f"Question {i}")

        st.info(question)

        answer = st.text_area(
            f"Your Answer {i}",
            key=f"answer_{i}",
            height=120
        )

        answers.append(answer)

    if st.button(
        "📝 Evaluate My Interview",
        key="evaluate_btn"
    ):

        try:

            response = requests.post(
                "http://127.0.0.1:8000/evaluate-interview",
                json={
                    "language": language,
                    "code": code,
                    "questions": st.session_state["questions"],
                    "answers": answers
                }
            )

            if response.status_code == 200:

                evaluation = response.json()

                st.success("Interview Evaluated!")

                st.metric(
                    "Overall Score",
                    f"{evaluation['overall_score']}/10"
                )

                st.progress(evaluation["overall_score"] / 10)

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Communication",
                    evaluation["communication"]
                )

                col2.metric(
                    "Technical Accuracy",
                    evaluation["technical_accuracy"]
                )

                col3.metric(
                    "Problem Solving",
                    evaluation["problem_solving"]
                )

                st.subheader("Feedback")

                for item in evaluation["feedback"]:
                    st.success(item)

                st.subheader("Recommendation")

                st.info(evaluation["recommendation"])

            else:

                st.error(response.text)

        except Exception as e:

            st.error(e)

    if st.button("🗑 Clear History"):
        with open("history.json", "w") as f:
            json.dump([], f)
        st.success("History cleared.")
        st.rerun()

    if os.path.exists("history.json"):
        with open("history.json", "r") as f:
            history = json.load(f)

        if len(history) == 0:
            st.info("No analysis history found.")
        else:
            for item in reversed(history):
                with st.expander(
                    f"{item['timestamp']} | {item['language']} | {item['score']}/100"
                ):
                    st.write(f"**Level:** {item['level']}")
                    st.write(f"**Time Complexity:** {item['time_complexity']}")
                    st.write(f"**Space Complexity:** {item['space_complexity']}")
    else:
        st.info("No history available.")

elif page == "📄 Code Mentor":

        st.title("📄 AI Code Mentor")

        language = st.selectbox(
            "Programming Language",
            ["Python", "Java", "C++", "JavaScript"],
            key="mentor_language"
        )

        code = st.text_area(
            "Paste your code",
            height=300,
            key="mentor_code"
        )

        if st.button("🔍 Review My Code"):

            if not code.strip():
                st.warning("Please paste your code.")

            else:

                with st.spinner("Reviewing code..."):

                    try:

                        response = requests.post(
                            "http://127.0.0.1:8000/review-code",
                            json={
                                "language": language,
                                "code": code
                            }
                        )

                        if response.status_code == 200:

                            result = response.json()
                            st.metric(
                                "⭐ Overall Code Quality",
                                f"{result['overall_score']}/100"
                            )

                            st.progress(result["overall_score"] / 100)

                            st.info(result["summary"])

                            st.divider()

                            st.success("Review Complete!")

                            for review in result["line_reviews"]:

                                severity = review["severity"]

                                if severity == "High":
                                    st.error(f"🔴 Line {review['line']}")
                                elif severity == "Medium":
                                    st.warning(f"🟠 Line {review['line']}")
                                else:
                                    st.success(f"🟢 Line {review['line']}")

                                st.code(review["code"], language.lower())

                                st.write(f"**Issue:** {review['issue']}")
                                st.write(f"**Suggestion:** {review['suggestion']}")

                        else:
                            st.error(response.text)

                    except Exception as e:
                        st.error(e)

# ---------------------------------
# About Page
# ---------------------------------
elif page == "ℹ About":
    st.title("ℹ About")
    st.write(f"What's My Level? {APP_VERSION}")
    st.markdown("""
An AI-powered coding assessment platform that analyzes your code,
estimates your skill level, and provides personalized interview
feedback and improvement suggestions.

**Built with:**
- Streamlit (frontend)
- FastAPI (backend)
- Gemini 2.5 Flash (AI engine)
""")

# ---------------------------------
# Home Page
# ---------------------------------
elif page == "🏠 Home":
    st.title("🚀 What's My Level?")
    st.markdown("""
### Know your coding level before the interviewer does.

Paste your code below and receive AI-powered feedback,
complexity analysis, and interview questions.
""")
    st.divider()

    # Language Selection
    language = st.selectbox(
        "Programming Language",
        ["Python", "Java", "C++", "JavaScript"]
    )

    # Code Input
    code = st.text_area(
        "Paste your code here",
        height=400,
        placeholder="Paste your solution here...",
        help="Supports Python, Java, C++, and JavaScript."
    )

    # Analyze Button
    analyze = st.button(
        "🚀 Analyze My Level",
        disabled=(code.strip() == "")
    )

    if analyze:
        with st.spinner("🤖 AI is analyzing your code..."):
            st.toast("Sending code to Gemini...", icon="🚀")
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json={
                        "language": language,
                        "code": code
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()

                    st.balloons()
                    st.toast("Analysis Complete!", icon="✅")
                    st.success("✅ Analysis Complete!")

                    # Level + Score
                    col1, col2 = st.columns(2)
                    level = result["level"].lower()

                    with col1:
                        if level == "beginner":
                            st.error("🔴 Beginner")
                        elif level == "intermediate":
                            st.warning("🟡 Intermediate")
                        elif level == "advanced":
                            st.success("🟢 Advanced")
                        else:
                            st.info(result["level"])

                    with col2:
                        st.metric("⭐ Score", f"{result['score']}/100")

                    st.progress(result["score"] / 100)
                    st.divider()

                    # Complexity
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("⏱ Time Complexity")
                        st.code(result["time_complexity"])
                    with col2:
                        st.subheader("💾 Space Complexity")
                        st.code(result["space_complexity"])

                    # Strengths & Weaknesses
                    with st.expander("✅ Strengths", expanded=True):
                        for strength in result.get("strengths", []):
                            st.success(strength)

                    with st.expander("⚠ Weaknesses"):
                        for weakness in result.get("weaknesses", []):
                            st.warning(weakness)

                    # Interview Question
                    st.subheader("🎤 Interview Question")
                    st.info(result["interview_question"])

                    # Optimization Suggestions
                    st.subheader("🚀 Optimization Suggestions")
                    for item in result.get("optimization_suggestions", []):
                        st.success(item)

                    # Save to history
                    history_entry = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "language": language,
                        "level": result["level"],
                        "score": result["score"],
                        "time_complexity": result["time_complexity"],
                        "space_complexity": result["space_complexity"],
                    }
                    history = []
                    if os.path.exists("history.json"):
                        with open("history.json", "r") as f:
                            history = json.load(f)
                    history.append(history_entry)
                    with open("history.json", "w") as f:
                        json.dump(history, f, indent=2)

                else:
                    st.error(f"❌ Backend returned an error: {response.status_code}")

            except Exception as e:
                st.error(f"❌ Connection Error: {e}")
                st.stop()

# ---------------------------------
# Footer
# ---------------------------------
st.divider()
st.caption("Built with ❤️ using Streamlit, FastAPI & Gemini AI")