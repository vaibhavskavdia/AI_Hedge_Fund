import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

st.title("⚠️ Risk Analytics")

try:

    response = requests.get(f"{API_URL}/portfolio")

    portfolio = response.json()

    if not portfolio:
        st.warning("No portfolio data available.")
        st.stop()

    # ------------------------
    # Build Risk Table
    # ------------------------

    risk_rows = []

    for position in portfolio:

        ticker = position.get("ticker", "N/A")

        probability = position.get(
            "prediction_probability",
            0.5
        )

        risk_score = round((1 - probability) * 100, 2)

        if risk_score < 30:
            risk_level = "LOW"

        elif risk_score < 60:
            risk_level = "MEDIUM"

        else:
            risk_level = "HIGH"

        risk_rows.append({
            "Ticker": ticker,
            "Risk Score": risk_score,
            "Risk Level": risk_level
        })

    risk_df = pd.DataFrame(risk_rows)

    # ------------------------
    # Summary Metrics
    # ------------------------

    avg_risk = round(
        risk_df["Risk Score"].mean(),
        2
    )

    highest_risk = risk_df.loc[
        risk_df["Risk Score"].idxmax(),
        "Ticker"
    ]

    lowest_risk = risk_df.loc[
        risk_df["Risk Score"].idxmin(),
        "Ticker"
    ]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Risk",
        f"{avg_risk}"
    )

    c2.metric(
        "Highest Risk",
        highest_risk
    )

    c3.metric(
        "Lowest Risk",
        lowest_risk
    )

    st.divider()

    # ------------------------
    # Risk Chart
    # ------------------------

    st.subheader("Portfolio Risk Distribution")

    fig = px.bar(
        risk_df,
        x="Ticker",
        y="Risk Score",
        color="Risk Level",
        title="Risk by Position"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ------------------------
    # Risk Table
    # ------------------------

    st.subheader("Risk Breakdown")

    st.dataframe(
        risk_df,
        use_container_width=True
    )

    st.divider()

    # ------------------------
    # Individual Position Cards
    # ------------------------

    st.subheader("Position Risk Analysis")

    for _, row in risk_df.iterrows():

        with st.expander(
            f"{row['Ticker']} | {row['Risk Level']} Risk"
        ):

            st.progress(
                min(row["Risk Score"] / 100, 1.0)
            )

            st.write(
                f"Risk Score: {row['Risk Score']}"
            )

            st.write(
                f"Risk Level: {row['Risk Level']}"
            )

except Exception as e:

    st.error(str(e))