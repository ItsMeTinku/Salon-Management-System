# database.py
import psycopg2
from psycopg2 import extras
import streamlit as st

# ─────────────────────────────────────────────────────────────────
# CENTRALIZED DATABASE CONNECTION
# ─────────────────────────────────────────────────────────────────

def get_connection():
    """Establish and return a connection to the Supabase PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            port=st.secrets["DB_PORT"]
        )
        return conn
    except Exception as e:
        st.error(f"Failed to connect to the database: {e}")
        return None

# ─────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS FOR CLEANER CODE
# ─────────────────────────────────────────────────────────────────

def execute_query(query, params=None):
    """Execute a query (INSERT, UPDATE, DELETE) and commit changes."""
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
            return True
    except Exception as e:
        st.error(f"Database Error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def fetch_all(query, params=None):
    """Fetch all rows for a given query."""
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
    finally:
        conn.close()

def fetch_one(query, params=None):
    """Fetch a single row for a given query."""
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
    finally:
        conn.close()

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