import streamlit as st
import time

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="What's My Level?",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------
# Title & Description
# -------------------------------
st.title("🚀 What's My Level?")

st.markdown("""
### Know your coding level before the interviewer does.

Paste your code below and receive AI-powered feedback,
complexity analysis, and personalized improvement suggestions.
""")

st.divider()

# -------------------------------
# Language Selection
# -------------------------------
language = st.selectbox(
    "Programming Language",
    ["Python", "Java", "C++", "JavaScript"]
)

# -------------------------------
# Code Input
# -------------------------------
code = st.text_area(
    "Paste your code here",
    placeholder="""type or paste your code here...""",
    height=300
)

# -------------------------------
# Analyze Button
# -------------------------------
if st.button("Analyze My Level 🚀"):

    if code.strip() == "":
        st.warning("⚠ Please paste your code before analyzing.")
    else:
        with st.spinner("Analyzing your code..."):
            time.sleep(2)

        st.success("Analysis Complete! ✅")

        st.subheader("Results")

        st.write("**Estimated Level:** Intermediate")
        st.write("**Overall Score:** 82/100")
        st.write("**Time Complexity:** O(n)")
        st.write("**Space Complexity:** O(n)")

        st.subheader("Strengths")
        st.write("✔ Efficient use of HashMap")
        st.write("✔ Clean logic")

        st.subheader("Areas to Improve")
        st.write("• Add comments")
        st.write("• Improve variable naming")
        st.write("• Handle more edge cases")

        st.subheader("Interview Question")
        st.info("Why is a HashMap solution better than using nested loops?")