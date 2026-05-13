import streamlit as st
from database import fetch_one

def init_session():
    """Ensure session state keys are initialized without triggering reruns."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "role" not in st.session_state:
        st.session_state.role = None

def login_page():
    st.title("💇 Salon ERP Login")

    # Use a container to keep the layout stable
    with st.container():
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        role = st.selectbox("Login as", ["Admin", "Staff"], key="login_role")

        if st.button("Login", use_container_width=True):
            try:
                # Direct fetch for auth (not cached as it's a security check)
                user = fetch_one(
                    "SELECT * FROM admin WHERE username=%s AND password=%s",
                    (username, password)
                )

                if user:
                    st.session_state.logged_in = True
                    st.session_state.role = role
                    st.success("Login Successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid Credentials. Please try again.")
            except Exception as e:
                st.error(f"Login error: {e}")

def logout():
    """Clear session and reset state."""
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.page = "Dashboard"
    st.rerun()