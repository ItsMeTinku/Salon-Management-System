# database.py
import os
import sqlite3

# ─────────────────────────────────────────────────────────────────
# Auto-detect which database backend to use.
#
#   Priority:
#     1. DATABASE_URL in Streamlit secrets  →  PostgreSQL (hosted, persistent)
#     2. DATABASE_URL environment variable  →  PostgreSQL (self-hosted)
#     3. Nothing set                        →  SQLite (local dev only)
# ─────────────────────────────────────────────────────────────────

_db_url = None

try:
    import streamlit as st
    _db_url = st.secrets.get("DATABASE_URL", None)
except Exception:
    pass

if not _db_url:
    _db_url = os.environ.get("DATABASE_URL", None)

# ─────────────────────────────────────────────────────────────────
# PostgreSQL Mode  (Supabase / Aiven / Neon / any hosted Postgres)
# ─────────────────────────────────────────────────────────────────
if _db_url:
    import psycopg2
    import streamlit as st

    USE_POSTGRES = True
    PH = "%s"          # psycopg2 placeholder

    @st.cache_resource
    def _init_pg_conn(url: str):
        """Cached PostgreSQL connection — reused across Streamlit reruns."""
        return psycopg2.connect(url, sslmode="require")

    conn = _init_pg_conn(_db_url)

# ─────────────────────────────────────────────────────────────────
# SQLite Mode  (local development — no setup needed)
# ─────────────────────────────────────────────────────────────────
else:
    USE_POSTGRES = False
    PH = "?"           # sqlite3 placeholder

    if os.path.isdir("/tmp") and os.access("/tmp", os.W_OK):
        _db_path = "/tmp/salon.db"
    else:
        _db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salon.db")

    conn = sqlite3.connect(_db_path, check_same_thread=False)

# Shared cursor
c = conn.cursor()

# ─────────────────────────────────────────────────────────────────
# Table Creation  (syntax works for both PostgreSQL and SQLite)
# ─────────────────────────────────────────────────────────────────
def create_tables():

    c.execute("""CREATE TABLE IF NOT EXISTS admin (
        username TEXT,
        password TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS employees (
        id TEXT PRIMARY KEY,
        name TEXT,
        profession TEXT,
        salary TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS attendance (
        emp_id TEXT,
        emp_name TEXT,
        status TEXT,
        date TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS customers (
        cust_name TEXT,
        phone TEXT,
        service TEXT,
        visit_date TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS appointments (
        cust_name TEXT,
        service TEXT,
        emp_id TEXT,
        date TEXT,
        status TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS billing (
        cust_name TEXT,
        service TEXT,
        amount TEXT,
        date TEXT
    )""")

    conn.commit()

# ─────────────────────────────────────────────────────────────────
# Default Admin Seed
# ─────────────────────────────────────────────────────────────────
def insert_admin():
    admin = c.execute("SELECT * FROM admin").fetchall()
    if not admin:
        c.execute(f"INSERT INTO admin VALUES ({PH}, {PH})", ("admin", "admin123"))
        conn.commit()