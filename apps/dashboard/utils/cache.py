import streamlit as st

from apps.dashboard.utils.api import (
    get_portfolio,
    get_latest_portfolio,
    get_portfolio_intelligence,
    get_risk,
)


class DashboardCache:

    def load(self):


        if "portfolio" not in st.session_state:
            st.session_state.portfolio = get_portfolio()

        if "latest_portfolio" not in st.session_state:
            st.session_state.latest_portfolio = get_latest_portfolio()

        if "portfolio_intelligence" not in st.session_state:
            st.session_state.portfolio_intelligence = (
                get_portfolio_intelligence()
            )

        if "risk" not in st.session_state:
            st.session_state.risk = get_risk()

    def refresh(self):

        st.session_state.backtest = get_backtest()

        st.session_state.portfolio = get_portfolio()

        st.session_state.latest_portfolio = (
            get_latest_portfolio()
        )

        st.session_state.portfolio_intelligence = (
            get_portfolio_intelligence()
        )

        st.session_state.risk = get_risk()


cache = DashboardCache()