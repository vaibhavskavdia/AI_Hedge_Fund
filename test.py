import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Plotly Test")

df = pd.DataFrame({
    "Ticker": ["META", "ORCL", "ADBE"],
    "Weight": [42.86, 28.57, 28.57],
})

st.dataframe(df)

fig = px.pie(
    df,
    names="Ticker",
    values="Weight",
)

st.plotly_chart(fig)

st.write("Finished")