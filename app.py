import streamlit as st
import pandas as pd

# Must be the first Streamlit command
st.set_page_config(
    page_title="Salon ERP Dashboard",
    page_icon="💇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS from style.py
from style import load_css
load_css()

from database import supabase_select
from auth import init_session, login_page, logout

# Standard modules
from employee import employee_module
from customer import customer_module
from appointment import appointment_module
from attendance import attendance_module
from billing import billing_module
from search import global_search

# ================= INIT =================
# Removed raw database table creation checks (startup_checks). 
# Supabase tables should be created via SQL Editor using supabase_setup.sql.

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
    st.rerun()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>💇 Salon ERP</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Display user info nicely
    role_color = "#22c55e" if st.session_state.get('role') == 'Admin' else "#3b82f6"
    username = st.session_state.get('username', 'User')
    st.markdown(f"""
    <div style="background-color: #1e293b; padding: 10px; border-radius: 8px; margin-bottom: 20px;">
        <span style="color: #94a3b8; font-size: 12px;">Logged in as:</span><br/>
        <strong style="color: white; font-size: 16px;">{username}</strong> 
        <span style="color: {role_color}; font-size: 12px; font-weight: bold; background: #0f172a; padding: 2px 6px; border-radius: 4px;">{st.session_state.get('role', 'Staff')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom stylized navigation
    nav_options = {
        "Dashboard": "📊 Dashboard",
        "Appointments": "📅 Appointments",
        "Customers": "🧾 Customers",
        "Billing": "💰 Billing",
        "Employees": "👩‍💼 Employees",
        "Attendance": "📌 Attendance",
        "Search": "🔍 Search"
    }
    
    for page_key, label in nav_options.items():
        # Highlight active page
        btn_type = "primary" if st.session_state.page == page_key else "secondary"
        if st.button(label, use_container_width=True, type=btn_type):
            navigate(page_key)
            
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        logout()

# ================= DASHBOARD =================
def dashboard():
    st.markdown("<h1 style='color: #0f172a;'>📊 Business Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Overview of salon performance and metrics.")

    # Fetch data using Supabase helper functions
    try:
        employees = supabase_select("employees")
        emp_count = len(employees) if employees else 0
        
        customers = supabase_select("customers")
        cust_count = len(customers) if customers else 0
        
        appointments = supabase_select("appointments")
        app_count = len(appointments) if appointments else 0
        
        billing = supabase_select("billing")
        
        # Calculate revenue from billing data
        revenue = 0
        chart_data = []
        if billing:
            df = pd.DataFrame(billing)
            if "amount" in df.columns:
                revenue = pd.to_numeric(df["amount"], errors='coerce').sum()
            
            # Group by service for chart
            if "service" in df.columns:
                chart_df = df.groupby("service").size().reset_index(name="count")
                chart_data = chart_df.set_index("service")["count"].to_dict()

        # ---------- KPI CARDS ----------
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👩‍💼 Total Staff", emp_count)
        with col2:
            st.metric("🧾 Customers CRM", cust_count)
        with col3:
            st.metric("📅 Total Appointments", app_count)
        with col4:
            st.metric("💰 Total Revenue", f"₹{revenue:,.2f}")

        st.markdown("---")

        # ---------- ANALYTICS (MODERN) ----------
        col_chart, col_recent = st.columns([2, 1])
        
        with col_chart:
            st.markdown("### 📈 Revenue by Service")
            with st.container(border=True):
                if chart_data:
                    st.bar_chart(chart_data, height=350)
                else:
                    st.info("No billing data available yet to display charts.")
                    
        with col_recent:
            st.markdown("### 🔔 Today's Appointments")
            with st.container(border=True):
                if appointments:
                    app_df = pd.DataFrame(appointments)
                    if "date" in app_df.columns:
                        today_str = pd.Timestamp.today().strftime('%Y-%m-%d')
                        today_apps = app_df[app_df["date"] == today_str]
                        
                        if not today_apps.empty:
                            for _, row in today_apps.iterrows():
                                status_color = "green" if row.get('status') == 'Completed' else "orange"
                                st.markdown(f"""
                                <div style="padding: 10px; border-left: 4px solid {status_color}; background: #f8fafc; margin-bottom: 8px; border-radius: 4px;">
                                    <strong>{row.get('cust_name', 'Unknown')}</strong> - {row.get('service', '')}<br/>
                                    <span style="font-size: 12px; color: {status_color};">{row.get('status', '')}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.write("No appointments scheduled for today.")
                else:
                    st.write("No appointments found.")

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