"""
style.py — Global CSS matching the V3 screenshot UI + V4 mobile improvements
"""

import streamlit as st


def load_css() -> None:
    st.markdown("""
    <style>

    /* ══════════════════════════════════════════
       DESIGN TOKENS
    ══════════════════════════════════════════ */
    :root {
        --primary:       #4f46e5;
        --primary-dark:  #4338ca;
        --sidebar-bg:    #0f172a;
        --sidebar-text:  #cbd5e1;
        --bg:            #f8fafc;
        --card:          #ffffff;
        --border:        #e2e8f0;
        --text:          #1e293b;
        --muted:         #64748b;
        --green:         #22c55e;
        --blue:          #3b82f6;
        --radius:        10px;
        --transition:    0.18s ease;
    }

    /* ══════════════════════════════════════════
       GLOBAL PAGE
    ══════════════════════════════════════════ */
    .stApp {
        background: var(--bg);
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }
    @keyframes fadeIn {
        from { opacity:0; transform:translateY(5px); }
        to   { opacity:1; transform:translateY(0); }
    }
    .main .block-container {
        animation: fadeIn 0.3s ease forwards;
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 1200px;
    }
    h1, h2, h3, h4 {
        color: var(--text);
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    /* ══════════════════════════════════════════
       SIDEBAR  —  matches screenshot exactly
       Dark navy background, white/grey text,
       indigo active button, transparent inactive
    ══════════════════════════════════════════ */

    /* Sidebar container */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: var(--sidebar-bg) !important;
        padding-top: 1rem;
    }

    /* Every text node inside sidebar */
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: var(--sidebar-text) !important;
    }

    /* ── All sidebar buttons base style ── */
    [data-testid="stSidebar"] .stButton button {
        width:            100%          !important;
        text-align:       left          !important;
        padding:          0.6rem 1rem   !important;
        border-radius:    var(--radius) !important;
        border:           none          !important;
        font-size:        0.95rem       !important;
        font-weight:      500           !important;
        min-height:       44px          !important;
        margin-bottom:    2px           !important;
        transition:       background var(--transition), color var(--transition) !important;
        background:       transparent   !important;
        color:            var(--sidebar-text) !important;
        box-shadow:       none          !important;
    }

    /* ── Hover on inactive buttons ── */
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.07) !important;
        color: #ffffff !important;
    }

    /* ── ACTIVE button (primary type = current page) ──
       Matches the indigo filled button in the screenshot */
    [data-testid="stSidebar"] .stButton button[kind="primary"] {
        background:  var(--primary)  !important;
        color:       #ffffff         !important;
        font-weight: 600             !important;
        box-shadow:  0 4px 12px rgba(79,70,229,0.35) !important;
    }
    [data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
        background: var(--primary-dark) !important;
    }

    /* ── Sidebar divider ── */
    [data-testid="stSidebar"] hr {
        border-color: #1e293b !important;
        margin: 10px 0 !important;
    }

    /* Sidebar toggle is now handled by Streamlit natively */

    /* ══════════════════════════════════════════
       KPI METRIC CARDS  — matches screenshot
       White card, large bold number, grey label
    ══════════════════════════════════════════ */
    [data-testid="metric-container"] {
        background:    var(--card)   !important;
        border:        1px solid var(--border) !important;
        border-radius: 12px          !important;
        padding:       1.2rem        !important;
        box-shadow:    0 1px 4px rgba(0,0,0,0.06) !important;
        transition:    transform var(--transition), box-shadow var(--transition);
    }
    [data-testid="metric-container"]:hover {
        transform:  translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.09) !important;
    }
    [data-testid="stMetricLabel"] p {
        color:          var(--muted)  !important;
        font-size:      0.82rem       !important;
        font-weight:    600           !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] > div {
        color:       var(--text) !important;
        font-size:   2rem        !important;
        font-weight: 800         !important;
    }

    /* ══════════════════════════════════════════
       MAIN CONTENT BUTTONS
    ══════════════════════════════════════════ */
    .main .stButton button {
        min-height:    42px          !important;
        border-radius: var(--radius) !important;
        font-weight:   600           !important;
        transition:    all var(--transition) !important;
        font-size:     0.9rem        !important;
    }
    .main .stButton button[kind="primary"] {
        background: var(--primary) !important;
        color:      white          !important;
        border:     none           !important;
    }
    .main .stButton button[kind="primary"]:hover {
        background:  var(--primary-dark)           !important;
        box-shadow:  0 4px 12px rgba(79,70,229,0.35) !important;
        transform:   translateY(-1px)                !important;
    }

    /* ══════════════════════════════════════════
       INPUTS & FORMS
    ══════════════════════════════════════════ */
    [data-testid="stForm"] {
        background:    var(--card)   !important;
        border:        1px solid var(--border) !important;
        border-radius: 12px          !important;
        padding:       1.5rem        !important;
        box-shadow:    0 1px 4px rgba(0,0,0,0.05);
    }
    .stTextInput  input,
    .stNumberInput input,
    .stTextArea   textarea {
        border-radius: var(--radius) !important;
        border:        1.5px solid var(--border) !important;
        font-size:     0.9rem        !important;
        transition:    border-color var(--transition), box-shadow var(--transition);
    }
    .stTextInput  input:focus,
    .stNumberInput input:focus,
    .stTextArea   textarea:focus {
        border-color: var(--primary)                !important;
        box-shadow:   0 0 0 3px rgba(79,70,229,0.15) !important;
    }

    /* ══════════════════════════════════════════
       TABS  — matches screenshot tab style
    ══════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        gap:        6px;
        background: transparent;
        flex-wrap:  wrap;
    }
    .stTabs [data-baseweb="tab"] {
        height:           38px;
        background:       #f1f5f9;
        border-radius:    var(--radius);
        border:           none !important;
        font-weight:      600;
        color:            #475569;
        padding:          0 1rem;
        white-space:      nowrap;
        transition:       all var(--transition);
    }
    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color:      white          !important;
        box-shadow: 0 3px 8px rgba(79,70,229,0.25);
    }

    /* ══════════════════════════════════════════
       DATAFRAME / TABLES
    ══════════════════════════════════════════ */
    .stDataFrame {
        border-radius: 12px !important;
        overflow:      hidden;
        border:        1px solid var(--border);
        box-shadow:    0 1px 3px rgba(0,0,0,0.05);
    }
    .stDataFrame > div {
        overflow-x:                 auto !important;
        -webkit-overflow-scrolling: touch;
    }

    /* ══════════════════════════════════════════
       ALERTS
    ══════════════════════════════════════════ */
    .stSuccess { background:#f0fdf4 !important; color:#166534 !important; border:1px solid #bbf7d0 !important; border-radius:8px !important; }
    .stError   { background:#fef2f2 !important; color:#991b1b !important; border:1px solid #fecaca !important; border-radius:8px !important; }
    .stWarning { background:#fffbeb !important; color:#92400e !important; border:1px solid #fde68a !important; border-radius:8px !important; }
    .stInfo    { background:#eff6ff !important; color:#1e40af !important; border:1px solid #bfdbfe !important; border-radius:8px !important; }

    /* ══════════════════════════════════════════
       SIDEBAR TOGGLE BUTTONS
       Making sure the expand arrow is visible!
    ══════════════════════════════════════════ */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    section[data-testid="stSidebar"] button[kind="header"] {
        display: inline-flex !important;
        visibility: visible !important;
    }

    /* ══════════════════════════════════════════
       HIDE STREAMLIT CHROME
    ══════════════════════════════════════════ */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    /* We CANNOT hide the header, because the sidebar arrow lives inside it! */
    header { background: transparent !important; }
    header [data-testid="stToolbar"] { visibility: hidden !important; }

    /* ══════════════════════════════════════════
       MOBILE BOTTOM NAV  (hidden on desktop)
       Shown only when screen < 768 px
    ══════════════════════════════════════════ */
    .mobile-nav { display: none; }

    @media (max-width: 768px) {
        .mobile-nav {
            display:         flex          !important;
            position:        fixed;
            bottom:          0;
            left:            0;
            right:           0;
            z-index:         9999;
            background:      var(--sidebar-bg);
            border-top:      1px solid #1e293b;
            height:          60px;
            justify-content: space-around;
            align-items:     stretch;
            box-shadow:      0 -4px 16px rgba(0,0,0,0.35);
        }
        .mobile-nav a {
            display:                 flex;
            flex-direction:          column;
            align-items:             center;
            justify-content:         center;
            flex:                    1;
            color:                   #94a3b8;
            text-decoration:         none !important;
            font-size:               0.58rem;
            font-weight:             600;
            gap:                     2px;
            padding:                 6px 2px;
            border-top:              2px solid transparent;
            transition:              all 0.15s ease;
            -webkit-tap-highlight-color: transparent;
        }
        .mobile-nav a .nav-icon { font-size: 1.15rem; line-height: 1; }
        .mobile-nav a.active {
            color:            var(--primary);
            border-top-color: var(--primary);
            background:       rgba(79,70,229,0.1);
        }

        /* ── Content adjustments on mobile ── */
        .main .block-container {
            padding-left:   0.75rem !important;
            padding-right:  0.75rem !important;
            padding-bottom: 5rem   !important;
        }
        [data-testid="stMetricValue"] > div { font-size: 1.5rem !important; }
        [data-testid="stMetricLabel"] p     { font-size: 0.7rem !important; }

        /* Inputs: 16px stops iOS Safari auto-zoom */
        .stTextInput  input,
        .stNumberInput input,
        .stTextArea   textarea  { font-size: 16px !important; min-height: 48px !important; }
        .main .stButton button  { min-height: 48px !important; }

        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.2rem !important; }
        h3 { font-size: 1.05rem !important; }

        .stTabs [data-baseweb="tab-list"] {
            flex-wrap:    nowrap;
            overflow-x:   auto;
            padding-bottom: 3px;
            scrollbar-width: none;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }

        [data-testid="stForm"] { padding: 1rem !important; }
    }

    /* ══════════════════════════════════════════
       SCROLLBAR (desktop)
    ══════════════════════════════════════════ */
    ::-webkit-scrollbar       { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }

    </style>
    """, unsafe_allow_html=True)


# ─── Mobile Bottom Navigation Bar ────────────────────────────────
def mobile_bottom_nav(current_page: str) -> None:
    """
    Fixed bottom tab bar — only visible on screens < 768 px (CSS-controlled).
    Each tab is a plain <a href="?page=X"> link.
    Streamlit reads st.query_params on every rerun so no JS bridge is needed.
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
    items = ""
    for key, icon, label in pages:
        active = "active" if current_page == key else ""
        items += (
            f'<a href="?page={key}" class="{active}" title="{key}">'
            f'<span class="nav-icon">{icon}</span>'
            f'<span>{label}</span>'
            f'</a>'
        )
    st.markdown(f'<nav class="mobile-nav">{items}</nav>', unsafe_allow_html=True)
