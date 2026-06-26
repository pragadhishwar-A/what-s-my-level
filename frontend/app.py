import streamlit as st

st.title("What's My Level?")

st.write("Welcome to the AI Coding Coach 🚀")

st.sidebar.header("User Input")

user_input = st.sidebar.text_area("Describe your coding problem:")

if st.sidebar.button("Submit"):
    st.write("User Input:")
    st.write(user_input)