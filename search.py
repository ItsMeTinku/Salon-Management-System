import streamlit as st
import pandas as pd
from database import c

def global_search():

    st.title("🔍 Global Search System")

    query = st.text_input("Search anything (Employee / Customer / Appointment / Billing)")

    if st.button("Search"):

        st.subheader("Employees")
        emp = c.execute(
            "SELECT * FROM employees WHERE name LIKE ? OR id LIKE ?",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
        st.table(emp)

        st.subheader("Customers")
        cust = c.execute(
            "SELECT * FROM customers WHERE cust_name LIKE ? OR phone LIKE ?",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
        st.table(cust)

        st.subheader("Appointments")
        app = c.execute(
            "SELECT * FROM appointments WHERE cust_name LIKE ?",
            (f"%{query}%",)
        ).fetchall()
        st.table(app)

        st.subheader("Billing")
        bill = c.execute(
            "SELECT * FROM billing WHERE cust_name LIKE ?",
            (f"%{query}%",)
        ).fetchall()
        st.table(bill)