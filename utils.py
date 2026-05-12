import streamlit as st

def navigate(page, subpage=None):
    st.session_state.page = page
    st.session_state.subpage = subpage
    st.rerun()