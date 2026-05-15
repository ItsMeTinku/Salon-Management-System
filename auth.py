import streamlit as st
from database import supabase_select

def init_session():
    """Ensure session state keys are initialized without triggering reruns."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "role" not in st.session_state:
        st.session_state.role = None
    if "username" not in st.session_state:
        st.session_state.username = None

def login_page():
    st.markdown("<h1 style='text-align: center;'>💇 Salon ERP Login</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Welcome back! Please enter your credentials.</p>", unsafe_allow_html=True)

    # Use a container to keep the layout stable
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container(border=True):
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            role = st.selectbox("Login as", ["Admin", "Staff"], key="login_role")

            if st.button("Login", use_container_width=True, type="primary"):
                try:
                    # Direct fetch for auth using Supabase helper
                    users = supabase_select("admin", match_filter={"username": username, "password": password})
                    
                    # We might want to check the role as well if we have roles in the DB, 
                    # but for now we just verify credentials and set the selected role.
                    # Or better, read the role from the DB if it exists.
                    
                    if users and len(users) > 0:
                        user = users[0]
                        st.session_state.logged_in = True
                        # If DB has a role, use it, else use the dropdown value
                        st.session_state.role = user.get("role", role)
                        st.session_state.username = user.get("username")
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
    st.session_state.username = None
    st.session_state.page = "Dashboard"
    st.rerun()