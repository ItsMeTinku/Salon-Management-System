import streamlit as st
import pandas as pd
from database import fetch_all

def global_search():
    st.title("🔍 Global Search System")
    query = st.text_input("Search anything (Employee / Customer / Appointment / Billing)")

    if st.button("Search", use_container_width=True):
        if not query.strip():
            st.warning("Please enter a search term.")
            return

        like_query = f"%{query.strip()}%"

        try:
            st.subheader("👩‍💼 Employees")
            emp = fetch_all("SELECT * FROM employees WHERE name LIKE %s OR id LIKE %s", (like_query, like_query))
            if emp:
                st.dataframe(pd.DataFrame(emp, columns=["ID", "Name", "Profession", "Salary"]), use_container_width=True)
            else:
                st.info("No employees found.")

            st.subheader("🧾 Customers")
            cust = fetch_all("SELECT * FROM customers WHERE cust_name LIKE %s OR phone LIKE %s", (like_query, like_query))
            if cust:
                st.dataframe(pd.DataFrame(cust, columns=["Name", "Phone", "Service", "Date"]), use_container_width=True)
            else:
                st.info("No customers found.")

            st.subheader("📅 Appointments")
            app = fetch_all("SELECT * FROM appointments WHERE cust_name LIKE %s OR emp_id LIKE %s", (like_query, like_query))
            if app:
                st.dataframe(pd.DataFrame(app, columns=["Customer", "Service", "Employee ID", "Date", "Status"]), use_container_width=True)
            else:
                st.info("No appointments found.")

            st.subheader("💰 Billing")
            bill = fetch_all("SELECT * FROM billing WHERE cust_name LIKE %s OR service LIKE %s", (like_query, like_query))
            if bill:
                st.dataframe(pd.DataFrame(bill, columns=["Customer", "Service", "Amount", "Date"]), use_container_width=True)
            else:
                st.info("No billing records found.")

        except Exception as e:
            st.error(f"❌ Search error: {e}")