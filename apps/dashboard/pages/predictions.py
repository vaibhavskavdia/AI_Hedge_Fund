import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.title("📈 AI Predictions")

try:

    response = requests.get(
        f"{API_URL}/portfolio/"
    )

    portfolio = response.json()
    st.write(portfolio)
    rows = []

    st.title("📈 AI Predictions")

    for p in portfolio:

        ticker = p.get("ticker","N/A")
        signal = p.get("signal","N/A")
        confidence = round(p.get("confidence",0)*100,2)

        c1,c2,c3 = st.columns(3)

        c1.metric("Ticker",ticker)
        c2.metric("Prediction",signal)
        c3.metric("Confidence",f"{confidence}%")

        st.divider()
    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True
    )

except Exception as e:
    st.error(str(e))