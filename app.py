import streamlit as st
from database import create_tables, insert_admin, fetch_all, fetch_one
from auth import init_session, login_page, logout

from employee import employee_module
from customer import customer_module
from appointment import appointment_module
from attendance import attendance_module
from billing import billing_module
from search import global_search

# ================= INIT =================
# Ensure tables are created on startup in PostgreSQL
create_tables()
insert_admin()
init_session()

# ================= LOGIN =================
if not st.session_state.logged_in:
    login_page()
    st.stop()

# ================= STATE =================
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "subpage" not in st.session_state:
    st.session_state.subpage = None

# ================= NAVIGATION FUNCTION =================
def navigate(page, subpage=None):
    st.session_state.page = page
    st.session_state.subpage = subpage
    st.rerun()

# ================= SIDEBAR =================
st.sidebar.title("💇 Salon ERP System")

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Employees", "Customers", "Appointments", "Attendance", "Billing", "Search", "Logout"],
    index=["Dashboard", "Employees", "Customers", "Appointments", "Attendance", "Billing", "Search", "Logout"].index(st.session_state.page)
)

st.session_state.page = menu

# ================= LOGOUT =================
if st.session_state.page == "Logout":
    logout()

# ================= DASHBOARD =================
def dashboard():
    st.title("📊 Salon ERP Dashboard")

    try:
        # Fetching counts using helper functions
        emp_data = fetch_all("SELECT id FROM employees")
        cust_data = fetch_all("SELECT phone FROM customers")
        app_data = fetch_all("SELECT date FROM appointments")
        bill_data = fetch_all("SELECT amount FROM billing")

        emp = len(emp_data)
        cust = len(cust_data)
        app = len(app_data)
        bill = len(bill_data)

        # PostgreSQL uses CAST(column AS type) or column::type
        rev_row = fetch_one("SELECT SUM(CAST(amount AS INTEGER)) FROM billing")
        revenue = rev_row[0] if rev_row and rev_row[0] else 0

        # ---------- KPI CARDS ----------
        col1, col2, col3, col4 = st.columns(4)

        if col1.button(f"👩‍💼 Employees\n{emp}", use_container_width=True):
            navigate("Employees", "View")

        if col2.button(f"🧾 Customers\n{cust}", use_container_width=True):
            navigate("Customers", "View")

        if col3.button(f"📅 Appointments\n{app}", use_container_width=True):
            navigate("Appointments", "View")

        if col4.button(f"💰 Revenue\n₹{revenue}", use_container_width=True):
            navigate("Billing", "View")

        st.markdown("---")

        # ---------- ANALYTICS ----------
        st.subheader("📈 Business Analytics")

        data = fetch_all("""
            SELECT service, COUNT(*) 
            FROM billing 
            GROUP BY service
        """)

        if data:
            st.bar_chart({k: v for k, v in data})
        else:
            st.info("No billing data yet")

        # ---------- INSIGHTS ----------
        st.markdown("---")
        st.subheader("🧠 Smart Insights")

        top_service = fetch_one("""
            SELECT service, COUNT(service)
            FROM billing
            GROUP BY service
            ORDER BY COUNT(service) DESC
            LIMIT 1
        """)

        col1, col2 = st.columns(2)
        col1.metric("💰 Total Revenue", f"₹{revenue}")

        if top_service:
            col2.metric("🔥 Top Service", top_service[0])
        else:
            col2.metric("🔥 Top Service", "N/A")

    except Exception as e:
        st.error(f"Error loading dashboard data: {e}")

# ================= ROUTING =================
if st.session_state.page == "Dashboard":
    dashboard()

elif st.session_state.page == "Employees":
    employee_module()

elif st.session_state.page == "Customers":
    customer_module()

elif st.session_state.page == "Appointments":
    appointment_module()

elif st.session_state.page == "Attendance":
    attendance_module()

elif st.session_state.page == "Billing":
    billing_module()

elif st.session_state.page == "Search":
    global_search()