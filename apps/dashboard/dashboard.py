import streamlit as st

from apps.dashboard.utils.cache import cache

st.set_page_config(
    page_title="AI Hedge Fund",
    page_icon="📈",
    layout="wide"
)

# Load cached data
cache.load()

st.title("🚀 AI Hedge Fund")

try:

    bt = st.session_state.backtest

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Return",
            f"{bt['total_return']}%"
        )

    with col2:
        st.metric(
            "Sharpe Ratio",
            bt["sharpe_ratio"]
        )

    with col3:
        st.metric(
            "Max Drawdown",
            f"{bt['max_drawdown']}%"
        )

    with col4:
        st.metric(
            "Alpha vs SPY",
            f"{bt['alpha_vs_spy']}%"
        )

except Exception as e:

    st.error(str(e))

st.divider()

st.subheader("Platform Overview")

c1, c2 = st.columns(2)

with c1:

    st.success("✅ Research Copilot")
    st.success("✅ Portfolio Construction")
    st.success("✅ Investment Committee")

with c2:

    st.success("✅ Risk Engine")
    st.success("✅ Market Predictions")
    st.success("✅ Performance Analytics")

st.divider()

st.subheader("Project Status")

st.info("""
Multi-Agent AI Hedge Fund Platform

• Research Agent (RAG)

• Portfolio Manager

• Investment Committee

• Risk Engine

• Agent Memory

• FastAPI Backend

• PostgreSQL Database

• Streamlit Dashboard
""")