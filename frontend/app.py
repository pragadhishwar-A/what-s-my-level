import streamlit as st
import requests

st.set_page_config(
    page_title="What's My Level?",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 What's My Level?")

st.success("Analysis Complete!")

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

for item in result["strengths"]:
    st.success(item)

st.subheader("⚠ Weaknesses")

for item in result["weaknesses"]:
    st.warning(item)

st.subheader("🎤 Interview Question")

st.info(result["interview_question"])

st.divider()

language = st.selectbox(
    "Programming Language",
    ["Python", "Java", "C++", "JavaScript"]
)

code = st.text_area(
    "Paste your code here",
    height=300,
    placeholder="""type your code here..."""
)

if st.button("Analyze My Level 🚀"):

    if code.strip() == "":
        st.warning("Please paste your code.")
    else:

        with st.spinner("Analyzing..."):

            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={
                    "language": language,
                    "code": code
                }
            )

        if response.status_code == 200:

            result = response.json()

            st.success("Analysis Complete!")

            st.subheader("Results")

            st.write(f"### 🎯 Level: {result['level']}")

            st.write(f"### ⭐ Score: {result['score']}/100")

            st.write(f"Language: {result['language']}")

            st.write(f"Characters in Code: {result['code_length']}")

            st.write(f"Time Complexity: {result['time_complexity']}")

            st.write(f"Space Complexity: {result['space_complexity']}")

            st.info(result["feedback"])

        else:

            st.error("Backend Error")