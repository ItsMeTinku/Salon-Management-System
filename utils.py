"""
utils.py — Shared navigation utility
─────────────────────────────────────
navigate() now writes to BOTH st.session_state.page
AND st.query_params["page"] so the current page is
always reflected in the browser URL and survives refresh.
"""

import streamlit as st


def navigate(page: str, subpage: str | None = None) -> None:
    """
    Switch to a different page.

    Updates both st.session_state (for same-run routing) and
    st.query_params (so the URL reflects the page and survives
    browser refresh / the Back button).
    """
    st.session_state.page    = page
    st.session_state.subpage = subpage
    st.query_params["page"]  = page
    st.rerun()
