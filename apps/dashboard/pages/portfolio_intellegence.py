import streamlit as st
import requests
import plotly.express as px
import pandas as pd 

API_URL = "http://localhost:8000"

st.title("📊 Portfolio Intelligence")

# ==================================
# Load Portfolio
# ==================================

try:

    portfolio = requests.get(f"{API_URL}/portfolio/").json()

except Exception:

    st.error("Unable to connect to API")
    st.stop()

if not portfolio:
    st.warning("No portfolio available")
    st.stop()

# ==================================
# Portfolio Metrics
# ==================================

holdings = len(portfolio)

top_pick = max(portfolio,key=lambda x: x["prediction_probability"])

top_pick = top_pick["ticker"]

biggest_position = max(portfolio,key=lambda x: x["weight"])

biggest_position = biggest_position["ticker"]

portfolio_grade = "B+"

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Portfolio Grade",portfolio_grade)

with c2:
    st.metric("Top Pick",top_pick)

with c3:
    st.metric("Largest Position",biggest_position)

with c4:
    st.metric("Holdings",holdings)

st.divider()

# ==================================
# Allocation
# ==================================

st.subheader("Portfolio Allocation")

for position in portfolio:

    st.progress(float(position["weight"]))

    st.write(f"{position['ticker']} : "f"{round(position['weight']*100,2)}%")

st.divider()

# ==========================================
# AI Research Center
# ==========================================

st.divider()

st.subheader("🔍 AI Research Center")

tickers = [p["ticker"] for p in portfolio]

selected_ticker = st.selectbox("Select a stock",tickers)

alloc_df = pd.DataFrame(portfolio)

fig = px.pie(alloc_df,names="ticker",values="weight",title="Portfolio Allocation")

st.plotly_chart(fig,use_container_width=True)

if st.button("Generate Investment Memo"):

    with st.spinner("Generating research..."):

        try:

            response = requests.post(f"{API_URL}/research/",json={"question": f"Give a complete hedge fund style investment memo for {selected_ticker}"})

            report = response.json()

            st.success(f"Research generated for {selected_ticker}")

            st.markdown(report["answer"])

        except Exception as e:

            st.error(str(e))