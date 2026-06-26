import streamlit as st
import requests

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="What's My Level?",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------
# Title
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
    height=300,
    placeholder="""type or paste your code here...""",
)

# ---------------------------------
# Analyze Button
# ---------------------------------
if st.button("🚀 Analyze My Level"):

    if code.strip() == "":
        st.warning("⚠ Please paste your code first.")

    else:

        with st.spinner("Analyzing your code..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json={
                        "language": language,
                        "code": code
                    }
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success("✅ Analysis Complete!")

                    st.divider()

                    st.subheader("🎯 Level")
                    st.write(result["level"])

                    st.subheader("⭐ Score")
                    st.progress(result["score"] / 100)
                    st.write(f"{result['score']}/100")

                    st.subheader("⏱ Time Complexity")
                    st.code(result["time_complexity"])

                    st.subheader("💾 Space Complexity")
                    st.code(result["space_complexity"])

                    st.subheader("✅ Strengths")

                    for strength in result["strengths"]:
                        st.success(strength)

                    st.subheader("⚠ Weaknesses")

                    for weakness in result["weaknesses"]:
                        st.warning(weakness)

                    st.subheader("🎤 Interview Question")

                    st.info(result["interview_question"])

                else:
                    st.error("❌ Backend returned an error.")

            except Exception as e:
                st.error(f"❌ Connection Error: {e}")