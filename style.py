import streamlit as st

def load_css():
    st.markdown("""
    <style>
    /* ================= GLOBAL ================= */
    :root {
        --primary: #4f46e5;
        --primary-hover: #4338ca;
        --bg-color: #f8fafc;
        --sidebar-bg: #0f172a;
        --text-main: #1e293b;
        --card-bg: #ffffff;
    }

    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* ================= SIDEBAR ================= */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid #1e293b;
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        color: #e2e8f0 !important;
    }

    /* Sidebar Buttons (Navigation) */
    section[data-testid="stSidebar"] button {
        border-radius: 8px !important;
        transition: all 0.2s ease;
        margin-bottom: 4px;
        justify-content: flex-start !important;
        padding-left: 1rem !important;
    }

    section[data-testid="stSidebar"] button[kind="primary"] {
        background-color: var(--primary) !important;
        border: none !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] button[kind="secondary"] {
        background-color: transparent !important;
        border: 1px solid transparent !important;
        color: #cbd5e1 !important;
    }
    
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
    }

    /* ================= MAIN TITLE ================= */
    h1, h2, h3, h4 {
        color: var(--text-main);
        font-weight: 700;
        letter-spacing: -0.025em;
    }

    /* ================= METRIC CARDS ================= */
    div[data-testid="metric-container"] {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
    }
    
    div[data-testid="metric-container"] > div {
        align-items: flex-start;
    }

    /* Metric Label */
    div[data-testid="stMetricLabel"] p {
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Metric Value */
    div[data-testid="stMetricValue"] div {
        color: var(--text-main) !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
    }

    /* ================= BUTTONS (MAIN APP) ================= */
    .stApp button[kind="primary"] {
        background-color: var(--primary);
        color: white;
        border-radius: 8px !important;
        font-weight: 600;
        border: none;
        transition: all 0.2s;
    }

    .stApp button[kind="primary"]:hover {
        background-color: var(--primary-hover);
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.4);
    }

    /* ================= DATA TABLE ================= */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }

    /* ================= TABS ================= */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: #f1f5f9;
        border-radius: 8px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 16px;
        padding-right: 16px;
        border: none !important;
        font-weight: 600;
        color: #475569;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--primary) !important;
        color: white !important;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
    }

    /* ================= INPUTS & CONTAINERS ================= */
    div[data-testid="stForm"] {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        background-color: #ffffff;
        padding: 24px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }

    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 0.5rem 0.75rem !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2) !important;
    }

    /* ================= SUCCESS / ERROR ================= */
    .stSuccess {
        background-color: #f0fdf4 !important;
        color: #166534 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 8px !important;
    }

    .stError {
        background-color: #fef2f2 !important;
        color: #991b1b !important;
        border: 1px solid #fecaca !important;
        border-radius: 8px !important;
    }

    .stWarning {
        background-color: #fffbeb !important;
        color: #92400e !important;
        border: 1px solid #fde68a !important;
        border-radius: 8px !important;
    }

    .stInfo {
        background-color: #eff6ff !important;
        color: #1e40af !important;
        border: 1px solid #bfdbfe !important;
        border-radius: 8px !important;
    }

    /* ================= HIDE STREAMLIT BRANDING ================= */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    </style>
    """, unsafe_allow_html=True)