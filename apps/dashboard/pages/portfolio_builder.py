import sys
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parents[3]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import requests
import pandas as pd
import plotly.express as px
from shared.constants.universe import SP500_UNIVERSE
API_URL = "http://localhost:8000"

st.title("📊 Portfolio Builder")

# ==================================
# Available Stocks
# ==================================



selected_tickers = st.multiselect(
    "Select Stocks",
    SP500_UNIVERSE
)

# ==================================
# Build Portfolio
# ==================================

if st.button("🚀 Build AI Portfolio"):

    if len(selected_tickers) < 3:
        st.warning("Select at least 3 stocks")
        st.stop()

    with st.spinner("Building portfolio..."):

        response = requests.post(
            f"{API_URL}/portfolio/ai-portfolio",
            json={"tickers": selected_tickers}
        )

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        result = response.json()
        
        st.session_state["portfolio_id"] = result["portfolio_id"]
        st.session_state["portfolio"] = result["portfolio"]
        st.session_state["recommendations"] = result["recommendations"]
        st.session_state["committee_review"] = result["committee_review"]
        
        if "portfolio" in st.session_state:

            portfolio = st.session_state["portfolio"]
            committee = st.session_state["committee_review"]

            st.success("Portfolio Created")

            st.markdown("## Portfolio Summary")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Portfolio Rating",
                    committee.get("portfolio_rating", "N/A")
                )

            with c2:
                st.metric(
                    "Top Pick",
                    committee.get("top_pick", "N/A")
                )

            with c3:
                st.metric(
                    "Diversification",
                    committee.get("diversification", "N/A")
                )

            st.divider()

            st.markdown("### Portfolio Allocation")

            portfolio_df = pd.DataFrame(
                [
                    {
                        "Ticker": ticker,
                        "Weight": weight
                    }
                    for ticker, weight in portfolio.items()
                ]
            )

            st.dataframe(
                portfolio_df,
                use_container_width=True
            )

            fig = px.pie(
                portfolio_df,
                names="Ticker",
                values="Weight",
                title="Portfolio Allocation"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.divider()

            st.markdown("### Investment Committee Verdict")

            st.info(
                committee.get(
                    "committee_summary",
                    "No summary available"
                )
            )