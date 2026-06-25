import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

st.title("⚠️ Risk Analytics")

# ====================================
# Load Data
# ====================================

try:

    response = requests.get(
        f"{API_URL}/risk/latest"
    )

    data = response.json()

except Exception as e:

    st.error(str(e))
    st.stop()

if "error" in data:

    st.warning(data["error"])
    st.stop()

portfolio = data["portfolio"]
analysis = data

recommendations = analysis.get(
    "recommendations",
    []
)

# ====================================
# Summary Metrics
# ====================================

st.subheader(
    "Portfolio Risk Summary"
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Health Score",
        analysis["health_score"]
    )

with col2:

    st.metric(
        "Risk Level",
        analysis["risk_score"]
    )

with col3:

    st.metric(
        "Diversification",
        analysis["diversification"]
    )

with col4:

    st.metric(
        "Largest Holding",
        analysis["largest_holding"]
    )

# ====================================
# Health Meter
# ====================================

st.divider()

st.subheader(
    "Portfolio Health"
)

st.progress(
    analysis["health_score"] / 100
)

st.write(
    f"Health Score: {analysis['health_score']}/100"
)

# ====================================
# Sector Exposure
# ====================================

st.divider()

st.subheader(
    "Sector Exposure"
)

sector_df = pd.DataFrame(
    {
        "Sector":
            list(
                analysis["sector_exposure"].keys()
            ),

        "Weight":
            list(
                analysis["sector_exposure"].values()
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
    title="Sector Allocation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ====================================
# Sector Risk Metrics
# ====================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Largest Sector",
        analysis["largest_sector"]
    )

with col2:

    st.metric(
        "Sector Weight",
        f"{analysis['largest_sector_weight']}%"
    )

# ====================================
# Position Breakdown
# ====================================

st.divider()

st.subheader(
    "Portfolio Positions"
)

positions_df = pd.DataFrame(
    {
        "Ticker":
            list(portfolio.keys()),

        "Weight":
            list(portfolio.values())
    }
)

st.dataframe(
    positions_df,
    use_container_width=True
)

fig = px.bar(
    positions_df,
    x="Ticker",
    y="Weight",
    title="Portfolio Weights"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ====================================
# Concentration Warning
# ====================================

st.divider()

if analysis["risk_score"].lower() == "high":

    st.error(
        f"High concentration risk in "
        f"{analysis['largest_holding']}"
    )

elif analysis["risk_score"].lower() == "medium":

    st.warning(
        f"Moderate concentration risk in "
        f"{analysis['largest_holding']}"
    )

else:

    st.success(
        "Portfolio concentration is healthy"
    )

# ====================================
# Rebalancing Recommendation
# ====================================

st.divider()

st.subheader(
    "Rebalancing Recommendation"
)

st.warning(
    analysis["rebalance_action"]
)

# ====================================
# Portfolio Manager Commentary
# ====================================

st.divider()

st.subheader(
    "Portfolio Manager Commentary"
)

st.info(
    analysis["manager_commentary"]
)

# ====================================
# AI Recommendations
# ====================================

if recommendations:

    st.divider()

    st.subheader(
        "AI Recommendations"
    )

    rec_df = pd.DataFrame(
        recommendations
    )

    st.dataframe(
        rec_df[
            [
                "ticker",
                "rating",
                "conviction",
                "position_size",
                "horizon"
            ]
        ],
        use_container_width=True
    )

    # ===============================
    # Risk Heatmap
    # ===============================

    st.subheader(
        "Risk Heatmap"
    )

    heatmap_df = pd.DataFrame({

        "ticker":
            rec_df["ticker"],

        "risk_score":
            10 - rec_df["position_size"],

        "position_size":
            rec_df["position_size"]
    })

    fig = px.scatter(
        heatmap_df,
        x="position_size",
        y="risk_score",
        text="ticker",
        size="position_size",
        title="Risk vs Position Size"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ===============================
    # Conviction Distribution
    # ===============================

    st.subheader(
        "Conviction Breakdown"
    )

    conviction_fig = px.histogram(
        rec_df,
        x="conviction",
        title="Conviction Distribution"
    )

    st.plotly_chart(
        conviction_fig,
        use_container_width=True
    )

    # ===============================
    # High Conviction Ideas
    # ===============================

    high_conviction = rec_df[
        rec_df["conviction"] == "HIGH"
    ]

    if not high_conviction.empty:

        st.subheader(
            "High Conviction Ideas"
        )

        for _, row in high_conviction.iterrows():

            st.success(
                f"{row['ticker']} | "
                f"{row['rating']} | "
                f"{row['horizon']}"
            )

    # ===============================
    # Top Pick Deep Dive
    # ===============================

    top_pick = rec_df.iloc[0]

    st.divider()

    st.subheader(
        f"Top Pick Deep Dive: "
        f"{top_pick['ticker']}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### 📈 Bull Case"
        )

        st.success(
            top_pick["bull_case"]
        )

    with col2:

        st.markdown(
            "### 📉 Bear Case"
        )

        st.error(
            top_pick["bear_case"]
        )

    st.markdown(
        "### 📝 Recommendation"
    )

    st.info(
        top_pick["recommendation"]
    )

# ====================================
# Raw Data
# ====================================

st.divider()

with st.expander(
    "View Raw Risk Data"
):

    st.json(data)