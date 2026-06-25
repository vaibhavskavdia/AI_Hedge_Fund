import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

# =====================================================
# PAGE CONFIG
# =====================================================

st.title("🏛 Portfolio Intelligence")

# =====================================================
# LOAD PORTFOLIO INTELLIGENCE
# =====================================================

try:

    response = requests.get(
        f"{API_URL}/portfolio/portfolio-intelligence"
    )

    if response.status_code != 200:
        st.error("Unable to load portfolio intelligence")
        st.stop()

    data = response.json()

except Exception as e:

    st.error(str(e))
    st.stop()

# =====================================================
# EXTRACT DATA
# =====================================================
portfolio_id = data["portfolio_id"]
health_score = data["health_score"]
risk_score = data["risk_score"]
diversification = data["diversification"]
largest_holding = data["largest_holding"]
largest_weight = data["largest_weight"]
sector_exposure = data["sector_exposure"]
manager_commentary = data["manager_commentary"]
recommendations = data["recommendations"]
# =====================================================
# HEADER
# =====================================================

st.caption(
    f"Portfolio ID: {portfolio_id}"
)

# =====================================================
# SUMMARY
# =====================================================

st.subheader("Portfolio Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Health Score",
        health_score
    )

with col2:
    st.metric(
        "Risk Score",
        risk_score
    )

with col3:
    st.metric(
        "Diversification",
        diversification
    )

with col4:
    st.metric(
        "Largest Holding",
        largest_holding
    )

st.divider()

# =====================================================
# SECTOR EXPOSURE
# =====================================================

st.subheader("Sector Exposure")

sector_df = pd.DataFrame(
    {
        "Sector": list(
            sector_exposure.keys()
        ),
        "Weight": list(
            sector_exposure.values()
        )
    }
)

st.dataframe(
    sector_df,
    use_container_width=True
)

fig = px.pie(
    sector_df,
    names="Sector",
    values="Weight",
    title="Sector Exposure"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# CONCENTRATION RISK
# =====================================================

st.subheader("Concentration Risk")

st.warning(
    f"""
Largest Position: {largest_holding}

Portfolio Weight: {largest_weight:.2f}%
"""
)

st.divider()

# =====================================================
# PORTFOLIO MANAGER COMMENTARY
# =====================================================

st.subheader(
    "Portfolio Manager Commentary"
)

st.info(
    manager_commentary
)

st.divider()

# =====================================================
# HOLDINGS ANALYSIS
# =====================================================

st.subheader("Holdings Analysis")

holdings_df = pd.DataFrame(
    recommendations
)

if not holdings_df.empty:

    columns_to_show = [
        col
        for col in [
            "ticker",
            "rating",
            "conviction",
            "position_size",
            "horizon"
        ]
        if col in holdings_df.columns
    ]

    st.dataframe(
        holdings_df[columns_to_show],
        use_container_width=True
    )

st.divider()

# =====================================================
# CONVICTION BREAKDOWN
# =====================================================

if (
    not holdings_df.empty
    and "conviction" in holdings_df.columns
):

    st.subheader(
        "Conviction Breakdown"
    )

    conviction_counts = (
        holdings_df["conviction"]
        .value_counts()
        .reset_index()
    )

    conviction_counts.columns = [
        "Conviction",
        "Count"
    ]

    fig = px.bar(
        conviction_counts,
        x="Conviction",
        y="Count",
        title="Conviction Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =====================================================
# TOP PICK DEEP DIVE
# =====================================================

top_pick = largest_holding

top_stock = None

for recommendation in recommendations:

    if recommendation.get(
        "ticker"
    ) == top_pick:

        top_stock = recommendation
        break

if top_stock:

    st.subheader(
        f"Top Pick Deep Dive: {top_pick}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### 📈 Bull Case"
        )

        st.success(
            top_stock.get(
                "bull_case",
                "Not Available"
            )
        )

    with col2:

        st.markdown(
            "### 📉 Bear Case"
        )

        st.error(
            top_stock.get(
                "bear_case",
                "Not Available"
            )
        )

    st.markdown(
        "### 📝 Recommendation"
    )

    st.info(
        top_stock.get(
            "recommendation",
            "Not Available"
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Position Size",
            top_stock.get(
                "position_size",
                "N/A"
            )
        )

    with col2:

        st.metric(
            "Time Horizon",
            top_stock.get(
                "horizon",
                "N/A"
            )
        )

st.divider()

# =====================================================
# RAW DATA
# =====================================================

with st.expander(
    "View Raw Intelligence Data"
):

    st.json(data)