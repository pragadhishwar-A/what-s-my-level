import streamlit as st
import requests
import time
import json
import os


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
    st.write("v1.1.0")
    page = st.radio(
    "Navigation",
    ["🏠 Home", "📜 Analysis History", "ℹ About"]
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
    st.divider()
    st.subheader("📜 Recent Analyses")

if page == "🏠 Home":
    # Home page code
    ...

elif page == "📜 Analysis History":

    st.title("📜 Analysis History")

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

elif page == "ℹ About":
    st.title("ℹ About")
    st.write("What's My Level? v1.2")
# ---------------------------------
# Main Page
# ---------------------------------
st.title("🚀 What's My Level?")

st.markdown("""
### Know your coding level before the interviewer does.

Paste your code below and receive AI-powered feedback,
complexity analysis, and interview questions.
""")

st.divider()

# ---------------------------------
# Language Selection
# ---------------------------------
language = st.selectbox(
    "Programming Language",
    ["Python", "Java", "C++", "JavaScript"]
)

# ---------------------------------
# Code Input
# ---------------------------------
code = st.text_area(
    "Paste your code here",
    height=400,
    placeholder="Paste your solution here...",
    help="Supports Python, Java, C++, and JavaScript."
)

# ---------------------------------
# Analyze Button
# ---------------------------------
analyze = st.button(
    "🚀 Analyze My Level",
    disabled=(code.strip() == "")
)

if analyze:

    if code.strip() == "":
        st.warning("⚠ Please paste your code.")

    else:

       with st.spinner("🤖 AI is analyzing your code..."):
        st.toast("Sending code to Gemini...", icon="🚀")
        if st.button("🗑 reset"):
            st.rerun()
    try:
                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json={
                        "language": language,
                        "code": code
                    },
                    timeout=30
                )

                if response.status_code == 200:

                    result = response.json()
                    
                    st.balloons()
                    st.toast("Analysis Complete!", icon="✅")

                    st.success("✅ Analysis Complete!")

                    col1, col2 = st.columns(2)

                    with col1:
                     level = result["level"].lower()

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

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("⏱ Time Complexity")
                        st.code(result["time_complexity"])

                    with col2:
                        st.subheader("💾 Space Complexity")
                        st.code(result["space_complexity"])

                    with st.expander("✅ Strengths", expanded=True):
                        for strength in result["strengths"]:
                            st.success(strength)

                    with st.expander("⚠ Weaknesses"):
                        for weakness in result["weaknesses"]:
                            st.warning(weakness)

                    st.subheader("🎤 Interview Question")
                    st.info(result["interview_question"])

                else:
                    st.error("❌ Backend returned an error.")

    except Exception as e:
                st.error(f"❌ Connection Error: {e}")

# ---------------------------------
# Footer
# ---------------------------------
st.divider()
st.caption("Built with ❤️ using Streamlit, FastAPI & Gemini AI")