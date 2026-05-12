import streamlit as st

def load_css():

    st.markdown("""
    <style>

    /* ================= GLOBAL ================= */
    .stApp {
        background: #f4f7fb;
        font-family: 'Segoe UI', sans-serif;
    }

    /* ================= SIDEBAR ================= */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a, #111827);
        color: white;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Sidebar radio */
    .stRadio label {
        font-size: 15px !important;
    }

    /* ================= MAIN TITLE ================= */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
    }

    /* ================= METRIC CARDS ================= */
    div[data-testid="metric-container"] {
        background: white;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        border: 1px solid #eef2f7;
        transition: all 0.2s ease-in-out;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    }

    /* ================= BUTTONS ================= */
    button[kind="primary"] {
        background: linear-gradient(90deg, #2563eb, #4f46e5);
        color: white;
        border-radius: 10px !important;
        padding: 8px 16px;
        font-weight: 600;
        border: none;
    }

    button:hover {
        opacity: 0.9;
    }

    /* ================= DATA TABLE ================= */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }

    /* ================= CARD STYLE BLOCK ================= */
    .card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 15px;
    }

    /* ================= SUCCESS / ERROR ================= */
    .stSuccess {
        background-color: #ecfdf5;
    }

    .stError {
        background-color: #fef2f2;
    }

    /* ================= HIDE STREAMLIT BRANDING ================= */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    </style>
    """, unsafe_allow_html=True)