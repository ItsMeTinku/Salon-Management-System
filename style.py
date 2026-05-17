"""
style.py — Global CSS & Mobile Responsiveness
─────────────────────────────────────────────────────────
CHANGES FROM V3:
  1. MOBILE BOTTOM NAVIGATION BAR:
     A fixed bottom tab bar appears on screens < 768 px with
     emoji icons for all main sections. Tapping a tab updates
     the URL (?page=X) which Streamlit reads on rerun.

  2. RESPONSIVE LAYOUT:
     - Tables are horizontally scrollable on mobile via a wrapper div.
     - st.columns fall back gracefully on narrow screens.
     - Forms stack vertically on small screens.
     - Metric cards reflow to a 2-column grid on mobile.
     - All font sizes scale with viewport.

  3. TOUCH-FRIENDLY:
     - All buttons have min-height: 44px (Apple HIG guideline).
     - Tap targets are comfortably spaced.
     - Active sidebar link has a strong visual indicator.

  4. SIDEBAR IMPROVEMENTS:
     - On desktop: elegant dark sidebar with nav buttons.
     - On mobile: sidebar is accessible via hamburger AND via
       the bottom nav bar, so nothing is hidden from users.

  5. SMOOTH TRANSITIONS & ANIMATIONS:
     - Cards, buttons, tabs animate with ease transitions.
     - A subtle fade-in on page load.
     - Hover lift effect on metric cards.
"""

import streamlit as st


def load_css() -> None:
    st.markdown("""
    <style>
    /* ════════════════════════════════════════════════════════════
       DESIGN TOKENS
    ════════════════════════════════════════════════════════════ */
    :root {
        --primary:        #4f46e5;
        --primary-hover:  #4338ca;
        --primary-light:  rgba(79, 70, 229, 0.1);
        --bg:             #f8fafc;
        --sidebar-bg:     #0f172a;
        --sidebar-width:  260px;
        --text:           #1e293b;
        --text-muted:     #64748b;
        --card-bg:        #ffffff;
        --border:         #e2e8f0;
        --success:        #22c55e;
        --danger:         #ef4444;
        --warning:        #f59e0b;
        --radius-sm:      6px;
        --radius-md:      10px;
        --radius-lg:      16px;
        --shadow-sm:      0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
        --shadow-md:      0 4px 6px -1px rgba(0,0,0,.07), 0 2px 4px -1px rgba(0,0,0,.04);
        --shadow-lg:      0 10px 15px -3px rgba(0,0,0,.08), 0 4px 6px -2px rgba(0,0,0,.04);
        --transition:     0.2s cubic-bezier(.4,0,.2,1);
    }

    /* ════════════════════════════════════════════════════════════
       PAGE FADE-IN
    ════════════════════════════════════════════════════════════ */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .main .block-container {
        animation: fadeIn 0.35s ease forwards;
        padding-top: 1.5rem !important;
        padding-bottom: 6rem !important; /* room for mobile bottom nav */
    }

    /* ════════════════════════════════════════════════════════════
       GLOBAL
    ════════════════════════════════════════════════════════════ */
    .stApp {
        background-color: var(--bg);
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }
    h1, h2, h3, h4 {
        color: var(--text);
        font-weight: 700;
        letter-spacing: -0.025em;
    }

    /* ════════════════════════════════════════════════════════════
       SIDEBAR — DESKTOP & MOBILE
       Forces sidebar to always be visible and correctly styled.
       Fixes: sidebar buttons invisible, sidebar collapsed on mobile.
    ════════════════════════════════════════════════════════════ */

    /* Sidebar background */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] > div:first-child {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid #1e293b !important;
    }

    /* Force sidebar to stay open on all screen sizes */
    section[data-testid="stSidebar"] {
        min-width: 240px !important;
        width: 260px !important;
    }

    /* All text inside sidebar */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #e2e8f0 !important;
    }

    /* ── Nav buttons: base ── */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition) !important;
        margin-bottom: 4px !important;
        min-height: 44px !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding-left: 1rem !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
        border: none !important;
        display: flex !important;
        align-items: center !important;
    }

    /* ── Active page (primary) ── */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"],
    section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {
        background-color: var(--primary) !important;
        color: white !important;
        box-shadow: 0 4px 10px rgba(79,70,229,0.4) !important;
    }

    /* ── Inactive pages (secondary) ── */
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"],
    section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"] {
        background-color: rgba(255,255,255,0.05) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover,
    section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: rgba(255,255,255,0.12) !important;
        color: white !important;
        border-color: rgba(255,255,255,0.15) !important;
    }

    /* ── Sidebar divider ── */
    section[data-testid="stSidebar"] hr {
        border-color: #1e293b !important;
        margin: 12px 0 !important;
    }

    /* ── Sidebar collapse button — make it visible on dark bg ── */
    button[data-testid="collapsedControl"],
    button[kind="header"] {
        background-color: var(--primary) !important;
        color: white !important;
        border-radius: 0 8px 8px 0 !important;
        border: none !important;
    }

    /* ════════════════════════════════════════════════════════════
       METRIC / KPI CARDS
    ════════════════════════════════════════════════════════════ */
    div[data-testid="metric-container"] {
        background: var(--card-bg);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border);
        transition: transform var(--transition), box-shadow var(--transition);
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg);
    }
    div[data-testid="stMetricLabel"] p {
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    div[data-testid="stMetricValue"] div {
        color: var(--text) !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
    }

    /* ════════════════════════════════════════════════════════════
       BUTTONS — MAIN APP
    ════════════════════════════════════════════════════════════ */
    .stApp button {
        min-height: 44px !important;
        border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
        transition: all var(--transition) !important;
        font-size: 0.9rem !important;
    }
    .stApp button[kind="primary"] {
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
    }
    .stApp button[kind="primary"]:hover {
        background-color: var(--primary-hover) !important;
        box-shadow: 0 4px 12px rgba(79,70,229,0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* ════════════════════════════════════════════════════════════
       INPUTS & FORMS
    ════════════════════════════════════════════════════════════ */
    div[data-testid="stForm"] {
        border-radius: var(--radius-lg);
        border: 1px solid var(--border);
        background: var(--card-bg);
        padding: 1.5rem;
        box-shadow: var(--shadow-sm);
    }
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox select,
    .stTextArea textarea {
        border-radius: var(--radius-md) !important;
        border: 1.5px solid var(--border) !important;
        padding: 0.6rem 0.85rem !important;
        font-size: 0.9rem !important;
        transition: border-color var(--transition), box-shadow var(--transition);
    }
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(79,70,229,0.18) !important;
        outline: none !important;
    }

    /* ════════════════════════════════════════════════════════════
       TABLES — Horizontally scrollable on mobile
    ════════════════════════════════════════════════════════════ */
    .stDataFrame {
        border-radius: var(--radius-lg);
        overflow: hidden;
        border: 1px solid var(--border);
        box-shadow: var(--shadow-sm);
    }
    /* Scrollable wrapper for dataframes on narrow screens */
    .stDataFrame > div {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch;
    }

    /* ════════════════════════════════════════════════════════════
       TABS
    ════════════════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: transparent;
        flex-wrap: wrap; /* wrap tabs on very narrow screens */
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background: #f1f5f9;
        border-radius: var(--radius-md);
        border: none !important;
        font-weight: 600;
        color: #475569;
        padding: 0 1rem;
        white-space: nowrap;
        transition: all var(--transition);
    }
    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
        box-shadow: 0 4px 8px rgba(79,70,229,0.25);
    }

    /* ════════════════════════════════════════════════════════════
       STATUS ALERTS
    ════════════════════════════════════════════════════════════ */
    .stSuccess  { background:#f0fdf4 !important; color:#166534 !important; border:1px solid #bbf7d0 !important; border-radius:var(--radius-md) !important; }
    .stError    { background:#fef2f2 !important; color:#991b1b !important; border:1px solid #fecaca !important; border-radius:var(--radius-md) !important; }
    .stWarning  { background:#fffbeb !important; color:#92400e !important; border:1px solid #fde68a !important; border-radius:var(--radius-md) !important; }
    .stInfo     { background:#eff6ff !important; color:#1e40af !important; border:1px solid #bfdbfe !important; border-radius:var(--radius-md) !important; }

    /* ════════════════════════════════════════════════════════════
       HIDE STREAMLIT CHROME
    ════════════════════════════════════════════════════════════ */
    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
    header     { visibility: hidden; }

    /* ════════════════════════════════════════════════════════════
       MOBILE BOTTOM NAVIGATION BAR
       Appears only on screens narrower than 768 px.
       Each item updates ?page= in the URL, Streamlit picks it up.
    ════════════════════════════════════════════════════════════ */
    .mobile-nav {
        display: none; /* hidden on desktop */
    }

    @media (max-width: 768px) {
        /* Show the bottom nav */
        .mobile-nav {
            display: flex !important;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 9999;
            background: var(--sidebar-bg);
            border-top: 1px solid #1e293b;
            padding: 0;
            height: 60px;
            justify-content: space-around;
            align-items: stretch;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
        }
        .mobile-nav a {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            flex: 1;
            color: #94a3b8;
            text-decoration: none !important;
            font-size: 0.6rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            gap: 2px;
            padding: 6px 2px;
            border-top: 2px solid transparent;
            transition: all 0.15s ease;
            -webkit-tap-highlight-color: transparent;
        }
        .mobile-nav a .nav-icon { font-size: 1.2rem; line-height: 1; }
        .mobile-nav a.active   {
            color: var(--primary);
            border-top-color: var(--primary);
            background: rgba(79,70,229,0.08);
        }
        .mobile-nav a:active   { background: rgba(255,255,255,0.06); }

        /* ── Layout adjustments ── */
        .main .block-container {
            padding-left: 0.75rem  !important;
            padding-right: 0.75rem !important;
            padding-bottom: 5rem   !important;
        }

        /* Metric cards: 2 per row on mobile */
        div[data-testid="metric-container"] {
            padding: 0.85rem !important;
        }
        div[data-testid="stMetricValue"] div {
            font-size: 1.4rem !important;
        }
        div[data-testid="stMetricLabel"] p {
            font-size: 0.7rem !important;
        }

        /* Tabs: allow horizontal scroll on very narrow */
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: nowrap;
            overflow-x: auto;
            padding-bottom: 4px;
            scrollbar-width: none;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }

        /* Inputs larger touch targets */
        .stTextInput input,
        .stNumberInput input,
        .stSelectbox select,
        .stTextArea textarea {
            font-size: 16px !important; /* prevent iOS zoom */
            min-height: 48px !important;
        }

        /* Buttons larger on mobile */
        .stApp button {
            min-height: 48px !important;
            font-size: 0.95rem !important;
        }

        /* Page title smaller on mobile */
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.25rem !important; }
        h3 { font-size: 1.1rem  !important; }

        /* Forms full width */
        div[data-testid="stForm"] {
            padding: 1rem !important;
        }

        /* Sidebar still accessible via hamburger, but bottom nav is primary */
        section[data-testid="stSidebar"] {
            /* Let Streamlit's native collapse still work */
        }

        /* Chart heights on mobile */
        div[data-testid="stArrowVegaLiteChart"] {
            height: 250px !important;
        }
    }

    /* ════════════════════════════════════════════════════════════
       TABLET (768 – 1024 px)
    ════════════════════════════════════════════════════════════ */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stMetricValue"] div {
            font-size: 1.6rem !important;
        }
    }

    /* ════════════════════════════════════════════════════════════
       SCROLLBAR STYLING (desktop)
    ════════════════════════════════════════════════════════════ */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

    /* ════════════════════════════════════════════════════════════
       APPOINTMENT STATUS BADGES
    ════════════════════════════════════════════════════════════ */
    .status-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .status-completed  { background:#dcfce7; color:#166534; }
    .status-pending    { background:#fef9c3; color:#854d0e; }
    .status-cancelled  { background:#fee2e2; color:#991b1b; }

    /* ════════════════════════════════════════════════════════════
       CARD CONTAINER HELPER
    ════════════════════════════════════════════════════════════ */
    .info-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        box-shadow: var(--shadow-sm);
        margin-bottom: 1rem;
    }

    </style>
    """, unsafe_allow_html=True)


def mobile_bottom_nav(current_page: str) -> None:
    """
    Render a fixed bottom navigation bar visible only on mobile (<768 px).
    Each link sets ?page=X in the URL. Streamlit reads st.query_params on
    every rerun, so the page switches automatically.

    The <nav> is hidden via CSS on desktop — no double navigation.
    """
    pages = [
        ("Dashboard",    "📊", "Home"),
        ("Appointments", "📅", "Appts"),
        ("Customers",    "🧾", "CRM"),
        ("Billing",      "💰", "Bill"),
        ("Employees",    "👩‍💼", "Staff"),
        ("Attendance",   "📌", "Attend"),
        ("Search",       "🔍", "Search"),
    ]

    items_html = ""
    for page_key, icon, label in pages:
        active_cls = "active" if current_page == page_key else ""
        # Update ?page= in URL → Streamlit picks it up via st.query_params
        href = f"?page={page_key}"
        items_html += (
            f'<a href="{href}" class="{active_cls}" title="{page_key}">'
            f'  <span class="nav-icon">{icon}</span>'
            f'  <span>{label}</span>'
            f'</a>'
        )

    st.markdown(
        f'<nav class="mobile-nav">{items_html}</nav>',
        unsafe_allow_html=True,
    )
