import streamlit as st
import requests

st.title("🤖 AI Research Copilot")

question = st.text_area(
    "Ask a question",
    height=150)

if st.button("Generate Research"):

    with st.spinner("Researching..."):

        response = requests.post("http://127.0.0.1:8000/research/",json={"question": question})

        if response.status_code == 200:
            result = response.json()
            st.success("Research Complete")
            st.markdown(result["answer"])
            
        else:
            st.error(f"API Error: {response.status_code}")
            st.code(response.text)