import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.title("📈 Stock Intelligence")

ticker = st.text_input(
    "Ticker",
    value="AVGO"
)

if not ticker:
    st.stop()

try:

    response = requests.post(
    f"{API_URL}/portfolio/ai-recommendation",
    json={
        "ticker": ticker
    }
)

    
    data = response.json()

except Exception as e:

    st.error(str(e))
    st.stop()

# ====================================
# Header
# ====================================

st.subheader(
    f"{ticker} Intelligence Report"
)

signal = data["rating"]

confidence = data["conviction"]

position_size = data["position_size"]

horizon = data["horizon"]

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Signal",
        signal
    )

with col2:

    st.metric(
        "Conviction",
        confidence
    )

with col3:

    st.metric(
        "Position Size",
        f"{position_size}%"
    )

with col4:

    st.metric(
        "Horizon",
        horizon
    )

st.divider()

# ====================================
# Recommendation Summary
# ====================================

st.subheader(
    "AI Recommendation"
)

if signal == "BUY":

    st.success(
        data["recommendation"]
    )

elif signal == "SELL":

    st.error(
        data["recommendation"]
    )

else:

    st.warning(
        data["recommendation"]
    )

st.divider()

# ====================================
# Bull vs Bear
# ====================================

st.subheader(
    "Investment Thesis"
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        "### 📈 Bull Case"
    )

    st.success(
        data["bull_case"]
    )

with col2:

    st.markdown(
        "### 📉 Bear Case"
    )

    st.error(
        data["bear_case"]
    )

st.divider()

# ====================================
# Trade Setup
# ====================================

st.subheader(
    "Suggested Trade Setup"
)

if confidence == "HIGH":

    stop_loss = "8%"

elif confidence == "MEDIUM":

    stop_loss = "12%"

else:

    stop_loss = "15%"

trade_df = pd.DataFrame([
    {
        "Metric": "Signal",
        "Value": signal
    },
    {
        "Metric": "Conviction",
        "Value": confidence
    },
    {
        "Metric": "Position Size",
        "Value": f"{position_size}%"
    },
    {
        "Metric": "Investment Horizon",
        "Value": horizon
    },
    {
        "Metric": "Suggested Stop Loss",
        "Value": stop_loss
    }
])

st.dataframe(
    trade_df,
    use_container_width=True
)

st.divider()

# ====================================
# Raw JSON
# ====================================

with st.expander(
    "View Full Analysis"
):

    st.json(data)