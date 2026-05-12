import streamlit as st

from database import create_tables, insert_admin, c
from auth import init_session, login_page, logout

from employee import employee_module
from customer import customer_module
from appointment import appointment_module
from attendance import attendance_module
from billing import billing_module
from search import global_search

# ================= INIT =================
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

    # ---------- DATA ----------
    emp = len(c.execute("SELECT * FROM employees").fetchall())
    cust = len(c.execute("SELECT * FROM customers").fetchall())
    app = len(c.execute("SELECT * FROM appointments").fetchall())
    bill = len(c.execute("SELECT * FROM billing").fetchall())

    revenue = c.execute("SELECT SUM(CAST(amount AS INTEGER)) FROM billing").fetchone()[0]
    revenue = revenue if revenue else 0

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

    data = c.execute("""
        SELECT service, COUNT(*) 
        FROM billing 
        GROUP BY service
    """).fetchall()

    if data:
        st.bar_chart({k: v for k, v in data})
    else:
        st.info("No billing data yet")

    # ---------- INSIGHTS ----------
    st.markdown("---")
    st.subheader("🧠 Smart Insights")

    top_service = c.execute("""
        SELECT service, COUNT(service)
        FROM billing
        GROUP BY service
        ORDER BY COUNT(service) DESC
        LIMIT 1
    """).fetchone()

    col1, col2 = st.columns(2)

    col1.metric("💰 Total Revenue", f"₹{revenue}")

    if top_service:
        col2.metric("🔥 Top Service", top_service[0])
    else:
        col2.metric("🔥 Top Service", "N/A")

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