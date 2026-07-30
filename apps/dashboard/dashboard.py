import streamlit as st

from components.theme import (
    apply_theme,
    section_header,
)


# ----------------------------------------------------
# App Configuration
# ----------------------------------------------------

apply_theme()


# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        # 📈 AI Hedge Fund

        Institutional-grade AI investment platform.
        """
    )

    st.divider()

    st.page_link(
        "pages/portfolio.py",
        label="Portfolio",
        icon="💼",
    )

    st.page_link(
        "pages/research.py",
        label="Research",
        icon="🔍",
    )

    st.page_link(
        "pages/stock_intelligence.py",
        label="Stock Intelligence",
        icon="📊",
    )

    st.page_link(
        "pages/sector_intelligence.py",
        label="Sector Intelligence",
        icon="🏭",
    )

    st.page_link(
        "pages/portfolio_intelligence.py",
        label="Portfolio Intelligence",
        icon="🧠",
    )

    st.page_link(
        "pages/risk.py",
        label="Risk Analysis",
        icon="⚠️",
    )

    st.divider()

    st.caption("Version 1.0")


# ----------------------------------------------------
# Landing Page
# ----------------------------------------------------

section_header(
    "AI Hedge Fund",
    "Institutional AI-powered portfolio management platform",
)

left, right = st.columns([1.5, 1])

with left:

    st.markdown(
        """
### Welcome

Generate institutional-grade AI portfolios using:

- Machine Learning predictions
- AI equity research
- Portfolio optimization
- Investment committee review
- Portfolio intelligence
- Risk analytics

Use the navigation menu to begin building your portfolio.
"""
    )

with right:

    st.metric(
        "AI Models",
        "5",
    )

    st.metric(
        "Research Agents",
        "3",
    )

    st.metric(
        "Supported Sectors",
        "11",
    )

    st.metric(
        "Portfolio Engine",
        "Ready",
    )

st.divider()

st.info(
    "👈 Start by opening **Portfolio** from the sidebar to generate an AI portfolio."
)