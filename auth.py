import streamlit as st
from database import c, conn

def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "role" not in st.session_state:
        st.session_state.role = None

def login_page():

    st.title("💇 Salon ERP Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Login as", ["Admin", "Staff"])

    if st.button("Login"):

        user = c.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials")

def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()