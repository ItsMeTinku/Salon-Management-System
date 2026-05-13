# database.py
import psycopg2
from psycopg2 import extras
import streamlit as st

# ─────────────────────────────────────────────────────────────────
# SINGLETON DATABASE CONNECTION (CRITICAL PERFORMANCE)
# ─────────────────────────────────────────────────────────────────

@st.cache_resource
def get_connection():
    """
    Establish a connection once and reuse it across all interactions.
    This prevents the overhead of reconnecting on every Streamlit rerun.
    """
    try:
        conn = psycopg2.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            port=st.secrets["DB_PORT"]
        )
        # Ensure connection stays alive
        conn.autocommit = False 
        return conn
    except Exception as e:
        st.error(f"Failed to connect to the database: {e}")
        return None

# ─────────────────────────────────────────────────────────────────
# CACHE INVALIDATION UTILITY
# ─────────────────────────────────────────────────────────────────

def clear_db_cache():
    """Clear cached query data after a mutation (Insert/Update/Delete)."""
    st.cache_data.clear()

# ─────────────────────────────────────────────────────────────────
# OPTIMIZED HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────

def execute_query(query, params=None):
    """Execute mutations and automatically invalidate query caches."""
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
            # Success! Clear caches so View pages see the new data
            clear_db_cache()
            return True
    except Exception as e:
        st.error(f"Database Error: {e}")
        conn.rollback()
        return False

@st.cache_data(ttl=600) # Cache for 10 minutes or until invalidated
def fetch_all(query, params=None):
    """Fetch all rows with st.cache_data for instant UI response."""
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    except Exception as e:
        st.error(f"Database Fetch Error: {e}")
        return []

@st.cache_data(ttl=600)
def fetch_one(query, params=None):
    """Fetch a single row with caching."""
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()
    except Exception as e:
        st.error(f"Database Fetch Error: {e}")
        return None

# ─────────────────────────────────────────────────────────────────
# TABLE INITIALIZATION (PostgreSQL Syntax)
# ─────────────────────────────────────────────────────────────────

def create_tables():
    """Ensure all required tables exist in PostgreSQL."""
    queries = [
        """CREATE TABLE IF NOT EXISTS admin (
            username TEXT PRIMARY KEY,
            password TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS employees (
            id TEXT PRIMARY KEY,
            name TEXT,
            profession TEXT,
            salary TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS attendance (
            emp_id TEXT,
            emp_name TEXT,
            status TEXT,
            date TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS customers (
            cust_name TEXT,
            phone TEXT,
            service TEXT,
            visit_date TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS appointments (
            cust_name TEXT,
            service TEXT,
            emp_id TEXT,
            date TEXT,
            status TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS billing (
            cust_name TEXT,
            service TEXT,
            amount TEXT,
            date TEXT
        )"""
    ]
    for q in queries:
        execute_query(q)

def insert_admin():
    """Seed the default admin user."""
    exists = fetch_one("SELECT * FROM admin WHERE username = %s", ("admin",))
    if not exists:
        execute_query(
            "INSERT INTO admin (username, password) VALUES (%s, %s)",
            ("admin", "admin123")
        )