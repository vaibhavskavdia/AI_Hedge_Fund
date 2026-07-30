import streamlit as st

DEFAULTS = {
    "selected_tickers": [],
    "job_id": None,
}


def initialize():
    """
    Initialize Streamlit session state.
    Only store transient UI state here.
    Portfolio data always comes from the backend.
    """
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_job():
    """
    Clear the current background job.
    """
    st.session_state.job_id = None


def reset_selection():
    """
    Clear selected tickers.
    """
    st.session_state.selected_tickers = []


def reset():
    """
    Reset all session state managed by this module.
    """
    for key, value in DEFAULTS.items():
        st.session_state[key] = value