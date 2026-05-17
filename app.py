"""
app.py — Salon ERP Main Application
─────────────────────────────────────────────────────────
CHANGES FROM V3:
  1. SESSION PERSISTENCE:
     - `init_session()` now reads a signed cookie and restores
       username / role automatically on browser refresh.
     - Page is persisted in st.query_params (the URL), so the user
       lands on the same page after refresh — no redirect to Dashboard.
     - Logout clears both session state and the cookie.

  2. MOBILE NAVIGATION:
     - `mobile_bottom_nav()` injects a fixed bottom tab bar visible
       only on screens < 768 px via CSS media queries.
     - Each tab updates the URL query param (?page=X) which Streamlit
       reads via st.query_params on rerun — zero custom JS required.
     - The existing sidebar stays for desktop users.

  3. URL-DRIVEN ROUTING:
     - `navigate(page)` writes to both st.session_state.page AND
       st.query_params["page"], keeping them in sync at all times.
     - On every load, query_params are read and used to set the page,
       so back/forward browser navigation "just works".

  4. RESPONSIVE DASHBOARD:
     - KPI row uses 2 columns on narrow screens (controlled by CSS).
     - Charts and tables are responsive.
"""

import streamlit as st
import pandas as pd

# ── Page config MUST be first ──────────────────────────────────────
st.set_page_config(
    page_title="Salon ERP",
    page_icon="💇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS (includes mobile nav styles) ─────────────────────────
from style import load_css, mobile_bottom_nav
load_css()

# ── Database & Auth ────────────────────────────────────────────────
from database import supabase_select
from auth import init_session, login_page, logout

# ── Feature modules ────────────────────────────────────────────────
from employee   import employee_module
from customer   import customer_module
from appointment import appointment_module
from attendance import attendance_module
from billing    import billing_module
from search     import global_search

# ══════════════════════════════════════════════════════════════════
# STEP 1: Initialize / restore session (checks cookies + query params)
# ══════════════════════════════════════════════════════════════════
init_session()

# ══════════════════════════════════════════════════════════════════
# STEP 2: Login guard
# ══════════════════════════════════════════════════════════════════
if not st.session_state.get("logged_in", False):
    login_page()
    st.stop()

# ══════════════════════════════════════════════════════════════════
# STEP 3: Ensure page state is set (fallback to Dashboard)
# ══════════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "subpage" not in st.session_state:
    st.session_state.subpage = None

VALID_PAGES = [
    "Dashboard", "Appointments", "Customers",
    "Billing", "Employees", "Attendance", "Search",
]

# Sync from URL if coming from mobile bottom nav or browser back/fwd
_url_page = st.query_params.get("page", None)
if _url_page and _url_page in VALID_PAGES:
    st.session_state.page = _url_page

# ══════════════════════════════════════════════════════════════════
# NAVIGATION HELPER
# ══════════════════════════════════════════════════════════════════
def navigate(page: str, subpage: str | None = None) -> None:
    """Set page in both session_state AND query_params (URL)."""
    st.session_state.page    = page
    st.session_state.subpage = subpage
    st.query_params["page"]  = page   # survives browser refresh
    st.rerun()

# ══════════════════════════════════════════════════════════════════
# SIDEBAR (desktop primary nav + mobile secondary)
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    # ── Branding — matches screenshot header ──────────────────
    st.markdown("""
    <div style="text-align:center; padding:0.75rem 0 1.25rem;">
        <div style="font-size:2.2rem; line-height:1;">💇</div>
        <p style="
            color:white; font-size:1.25rem; font-weight:700;
            margin:6px 0 0; letter-spacing:-0.02em;
        ">Salon ERP</p>
    </div>
    """, unsafe_allow_html=True)

    # ── User info badge — matches screenshot exactly ──────────
    uname      = st.session_state.get("username", "User")
    urole      = st.session_state.get("role", "Staff")
    role_color = "#22c55e" if urole == "Admin" else "#3b82f6"
    st.markdown(f"""
    <div style="
        background:#1e293b; padding:10px 14px;
        border-radius:10px; margin-bottom:14px;
        border:1px solid #334155;
    ">
        <span style="color:#64748b; font-size:11px; font-weight:500;">
            Logged in as:
        </span><br/>
        <div style="display:flex; align-items:center; gap:8px; margin-top:4px;">
            <strong style="color:white; font-size:15px;">{uname}</strong>
            <span style="
                color:{role_color}; font-size:11px; font-weight:700;
                background:#0f172a; padding:2px 8px;
                border-radius:999px; border:1px solid {role_color}44;
            ">{urole}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Navigation — same labels as screenshot ────────────────
    nav_items = [
        ("Dashboard",    "📊 Dashboard"),
        ("Appointments", "📅 Appointments"),
        ("Customers",    "🧾 Customers"),
        ("Billing",      "💰 Billing"),
        ("Employees",    "👩‍💼 Employees"),
        ("Attendance",   "📌 Attendance"),
        ("Search",       "🔍 Search"),
    ]

    for page_key, label in nav_items:
        is_active = st.session_state.page == page_key
        if st.button(
            label,
            use_container_width=True,
            type="primary" if is_active else "secondary",
            key=f"nav_{page_key}",
        ):
            navigate(page_key)

    st.markdown(
        "<hr style='border-color:#1e293b; margin:14px 0 10px;'>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    <p style="color:#475569; font-size:11px; text-align:center; margin:0 0 8px;">
        🔒 Session valid for 7 days
    </p>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout"):
        logout()

# ══════════════════════════════════════════════════════════════════
# MOBILE BOTTOM NAV BAR (CSS-hidden on desktop)
# ══════════════════════════════════════════════════════════════════
mobile_bottom_nav(st.session_state.page)

# ══════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════
def dashboard() -> None:
    st.markdown(
        "<h1 style='color:#0f172a;'>📊 Business Dashboard</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#64748b;'>Overview of your salon performance.</p>",
        unsafe_allow_html=True,
    )

    try:
        employees    = supabase_select("employees")    or []
        customers    = supabase_select("customers")    or []
        appointments = supabase_select("appointments") or []
        billing      = supabase_select("billing")      or []

        emp_count  = len(employees)
        cust_count = len(customers)
        app_count  = len(appointments)
        revenue    = 0
        chart_data = {}

        if billing:
            df_bill = pd.DataFrame(billing)
            if "amount" in df_bill.columns:
                revenue = pd.to_numeric(df_bill["amount"], errors="coerce").sum()
            if "service" in df_bill.columns:
                chart_data = (
                    df_bill.groupby("service")
                    .size()
                    .reset_index(name="count")
                    .set_index("service")["count"]
                    .to_dict()
                )

        # ── KPI Cards — 4 columns (CSS reflows to 2 on mobile) ──────
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("👩‍💼 Total Staff",        emp_count)
        c2.metric("🧾 Customer CRM",         cust_count)
        c3.metric("📅 Total Appointments",   app_count)
        c4.metric("💰 Total Revenue",        f"₹{revenue:,.0f}")

        st.markdown("<hr style='margin:1.5rem 0; border-color:#e2e8f0;'>",
                    unsafe_allow_html=True)

        # ── Charts & Today's appointments ────────────────────────────
        col_chart, col_today = st.columns([2, 1])

        with col_chart:
            st.markdown("### 📈 Revenue by Service")
            with st.container(border=True):
                if chart_data:
                    st.bar_chart(chart_data, height=320)
                else:
                    st.info("No billing data yet — revenue chart will appear here.")

        with col_today:
            st.markdown("### 🔔 Today's Appointments")
            with st.container(border=True):
                if appointments:
                    df_app = pd.DataFrame(appointments)
                    if "date" in df_app.columns:
                        today = pd.Timestamp.today().strftime("%Y-%m-%d")
                        today_df = df_app[df_app["date"] == today]
                        if not today_df.empty:
                            for _, row in today_df.iterrows():
                                s = row.get("status", "Pending")
                                color = (
                                    "#22c55e" if s == "Completed" else
                                    "#ef4444" if s == "Cancelled" else
                                    "#f59e0b"
                                )
                                st.markdown(f"""
                                <div style="
                                    padding:10px 12px;
                                    border-left:4px solid {color};
                                    background:#f8fafc;
                                    margin-bottom:8px;
                                    border-radius:0 8px 8px 0;
                                ">
                                    <strong style="color:#1e293b;">
                                        {row.get('cust_name','Unknown')}
                                    </strong>
                                    <span style="color:#64748b; font-size:0.8rem;">
                                        — {row.get('service','')}
                                    </span><br/>
                                    <span style="color:{color}; font-size:0.75rem; font-weight:600;">
                                        {s}
                                    </span>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No appointments today.")
                    else:
                        st.info("No appointment data.")
                else:
                    st.info("No appointments found.")

        # ── Quick-access cards on mobile ─────────────────────────────
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        qa1, qa2, qa3, qa4 = st.columns(4)
        with qa1:
            if st.button("📅 New Appointment", use_container_width=True):
                navigate("Appointments")
        with qa2:
            if st.button("🧾 Add Customer", use_container_width=True):
                navigate("Customers")
        with qa3:
            if st.button("💰 Create Invoice", use_container_width=True):
                navigate("Billing")
        with qa4:
            if st.button("📌 Mark Attendance", use_container_width=True):
                navigate("Attendance")

    except Exception as e:
        st.error(f"Dashboard error: {e}")

# ══════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════
page = st.session_state.page

if   page == "Dashboard":    dashboard()
elif page == "Employees":    employee_module()
elif page == "Customers":    customer_module()
elif page == "Appointments": appointment_module()
elif page == "Attendance":   attendance_module()
elif page == "Billing":      billing_module()
elif page == "Search":       global_search()
else:
    st.warning(f"Unknown page: '{page}'. Redirecting to Dashboard.")
    navigate("Dashboard")
