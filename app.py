import streamlit as st
from database import create_tables, insert_admin, fetch_all, fetch_one
from auth import init_session, login_page, logout

# Standard modules
from employee import employee_module
from customer import customer_module
from appointment import appointment_module
from attendance import attendance_module
from billing import billing_module
from search import global_search

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Salon ERP Dashboard",
    page_icon="💇",
    layout="wide"
)

# ================= INIT =================
@st.cache_resource
def startup_checks():
    """Run table creation only once on startup."""
    create_tables()
    insert_admin()

startup_checks()
init_session()

# ================= LOGIN GUARD =================
if not st.session_state.get("logged_in", False):
    login_page()
    st.stop()

# ================= STABLE STATE =================
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "subpage" not in st.session_state:
    st.session_state.subpage = None

# ================= NAVIGATION FUNCTION =================
def navigate(page, subpage=None):
    st.session_state.page = page
    st.session_state.subpage = subpage
    # Use st.rerun sparingly to avoid flickers
    st.rerun()

# ================= SIDEBAR =================
with st.sidebar:
    st.title("💇 Salon ERP System")
    st.write(f"Logged as: **{st.session_state.get('role', 'Staff')}**")
    
    menu = st.radio(
        "Navigation",
        ["Dashboard", "Employees", "Customers", "Appointments", "Attendance", "Billing", "Search", "Logout"],
        index=["Dashboard", "Employees", "Customers", "Appointments", "Attendance", "Billing", "Search", "Logout"].index(st.session_state.page),
        key="main_nav"
    )

    if menu != st.session_state.page:
        st.session_state.page = menu
        st.rerun()

# ================= LOGOUT =================
if st.session_state.page == "Logout":
    logout()

# ================= DASHBOARD (CACHED) =================
def dashboard():
    st.title("📊 Salon ERP Dashboard")

    # Fetch data using cached helpers
    try:
        emp_count = len(fetch_all("SELECT id FROM employees"))
        cust_count = len(fetch_all("SELECT phone FROM customers"))
        app_count = len(fetch_all("SELECT date FROM appointments"))
        
        rev_row = fetch_one("SELECT SUM(CAST(amount AS INTEGER)) FROM billing")
        revenue = rev_row[0] if rev_row and rev_row[0] else 0

        # ---------- KPI CARDS ----------
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👩‍💼 Employees", emp_count)
            if st.button("Manage Staff", key="btn_emp"): navigate("Employees", "View")

        with col2:
            st.metric("🧾 Customers", cust_count)
            if st.button("Manage CRM", key="btn_cust"): navigate("Customers", "View")

        with col3:
            st.metric("📅 Appointments", app_count)
            if st.button("View Schedule", key="btn_app"): navigate("Appointments", "View")

        with col4:
            st.metric("💰 Total Revenue", f"₹{revenue}")
            if st.button("Billing History", key="btn_bill"): navigate("Billing", "View")

        st.markdown("---")

        # ---------- ANALYTICS (OPTIMIZED) ----------
        st.subheader("📈 Business Analytics")

        chart_data = fetch_all("""
            SELECT service, COUNT(*) 
            FROM billing 
            GROUP BY service
        """)

        if chart_data:
            st.bar_chart({k: v for k, v in chart_data})
        else:
            st.info("No billing data yet")

    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

# ================= ROUTING =================
page = st.session_state.page

if page == "Dashboard":
    dashboard()
elif page == "Employees":
    employee_module()
elif page == "Customers":
    customer_module()
elif page == "Appointments":
    appointment_module()
elif page == "Attendance":
    attendance_module()
elif page == "Billing":
    billing_module()
elif page == "Search":
    global_search()