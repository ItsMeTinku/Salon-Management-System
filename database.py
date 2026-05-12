# database.py

import sqlite3

# ---------- DATABASE CONNECTION ----------
conn = sqlite3.connect('salon.db', check_same_thread=False)
c = conn.cursor()

# ---------- CREATE TABLES ----------
def create_tables():

    c.execute('''CREATE TABLE IF NOT EXISTS admin (
        username TEXT,
        password TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id TEXT PRIMARY KEY,
        name TEXT,
        profession TEXT,
        salary TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        emp_id TEXT,
        emp_name TEXT,
        status TEXT,
        date TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS customers (
        cust_name TEXT,
        phone TEXT,
        service TEXT,
        visit_date TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
        cust_name TEXT,
        service TEXT,
        emp_id TEXT,
        date TEXT,
        status TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS billing (
        cust_name TEXT,
        service TEXT,
        amount TEXT,
        date TEXT
    )''')

    conn.commit()

# ---------- DEFAULT ADMIN ----------
def insert_admin():
    admin = c.execute("SELECT * FROM admin").fetchall()
    if not admin:
        c.execute("INSERT INTO admin VALUES (?, ?)", ('admin', 'admin123'))
        conn.commit()