import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.title("💼 Portfolio Construction")

response = requests.get(
    f"{API_URL}/portfolio"
)

portfolio = response.json()

if not portfolio:
    st.warning("No portfolio available")
    st.stop()

df = pd.DataFrame(portfolio)

st.dataframe(df,use_container_width=True)

st.subheader("Current Holdings")

for position in portfolio:

    ticker = position.get("ticker","N/A")
    weight = round(position.get("weight",0)*100,2)

    st.progress(weight/100)

    st.write(
        f"**{ticker}** : {weight}%"
    )