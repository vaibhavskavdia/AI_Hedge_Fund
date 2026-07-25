import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parents[3]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.constants.universe import SP500_UNIVERSE

API_URL = "http://localhost:8000"

st.title("📊 Portfolio Builder")

# -------------------------------------------------
# Session State
# -------------------------------------------------

defaults = {
    "selected_tickers": [],
    "portfolio": None,
    "portfolio_id": None,
    "recommendations": None,
    "committee_review": None,
    "is_generating": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------------------------------------
# Stock Selector
# -------------------------------------------------

selected = st.multiselect(
    "Select Stocks",
    SP500_UNIVERSE,
    default=st.session_state.selected_tickers,
)

st.session_state.selected_tickers = selected

# -------------------------------------------------
# Build Portfolio
# -------------------------------------------------

if st.button("🚀 Build AI Portfolio"):

    if len(selected) < 3:
        st.warning("Select at least 3 stocks")
        st.stop()

    st.session_state.is_generating = True

    with st.spinner("Building AI Portfolio..."):

        try:

            response = requests.post(
                f"{API_URL}/portfolio/ai-portfolio",
                json={"tickers": selected},
                timeout=600,
            )

            response.raise_for_status()

            result = response.json()

            st.session_state.portfolio_id = result["portfolio_id"]
            st.session_state.portfolio = result["portfolio"]
            st.session_state.recommendations = result["recommendations"]
            st.session_state.committee_review = result["committee_review"]

        except Exception as e:
            st.error(str(e))

        finally:
            st.session_state.is_generating = False

# -------------------------------------------------
# Generation Status
# -------------------------------------------------

if st.session_state.is_generating:
    st.info("⏳ Building a new portfolio... The previous portfolio remains available.")

# -------------------------------------------------
# Display Portfolio
# -------------------------------------------------

if st.session_state.portfolio is not None:

    portfolio = st.session_state.portfolio
    committee = st.session_state.committee_review

    st.success("Portfolio Ready")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Portfolio Rating",
        committee.get("portfolio_rating", "N/A"),
    )

    c2.metric(
        "Top Pick",
        committee.get("top_pick", "N/A"),
    )

    c3.metric(
        "Diversification",
        committee.get("diversification", "N/A"),
    )

    st.divider()

    portfolio_df = pd.DataFrame(
        [
            {
                "Ticker": ticker,
                "Weight": weight,
            }
            for ticker, weight in portfolio.items()
        ]
    )

    st.dataframe(
        portfolio_df,
        use_container_width=True,
    )

    fig = px.pie(
        portfolio_df,
        names="Ticker",
        values="Weight",
        title="Portfolio Allocation",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.divider()

    st.markdown("### Investment Committee Verdict")

    st.info(
        committee.get(
            "committee_summary",
            "No summary available",
        )
    )