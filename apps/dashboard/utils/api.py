import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"


def _get(endpoint: str):
    response = requests.get(f"{BASE_URL}{endpoint}")
    response.raise_for_status()
    return response.json()


def _post(endpoint: str, payload: dict):
    response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
    response.raise_for_status()
    return response.json()




# -----------------------
# Portfolio
# -----------------------

@st.cache_data(ttl=300)
def get_portfolio():
    return _get("/portfolio/")


@st.cache_data(ttl=300)
def get_latest_portfolio():
    return _get("/portfolio/latest")


@st.cache_data(ttl=300)
def get_portfolio_intelligence():
    return _get("/portfolio/portfolio-intelligence")


@st.cache_data(ttl=300)
def get_risk():
    return _get("/risk/latest")


# -----------------------
# AI Calls
# -----------------------

def generate_portfolio(tickers):
    return _post(
        "/portfolio/ai-portfolio",
        {
            "tickers": tickers
        },
    )


def generate_recommendation(ticker):
    return _post(
        "/portfolio/ai-recommendation",
        {
            "ticker": ticker
        },
    )


# -----------------------
# Cache Refresh
# -----------------------

def clear_all_cache():

    
    get_portfolio.clear()
    get_latest_portfolio.clear()
    get_portfolio_intelligence.clear()
    get_risk.clear()