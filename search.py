import streamlit as st
import pandas as pd
from database import fetch_all

def global_search():
    st.title("🔍 Unified Search")
    query = st.text_input("Search ID, Name, Phone, or Service...", key="global_search_input")

    if query.strip():
        like_query = f"%{query.strip()}%"
        
        try:
            # Employees
            emp = fetch_all("SELECT * FROM employees WHERE name LIKE %s OR id LIKE %s", (like_query, like_query))
            if emp:
                st.subheader("👩‍💼 Employees")
                st.dataframe(pd.DataFrame(emp, columns=["ID", "Name", "Profession", "Salary"]), use_container_width=True)

            # Customers
            cust = fetch_all("SELECT * FROM customers WHERE cust_name LIKE %s OR phone LIKE %s", (like_query, like_query))
            if cust:
                st.subheader("🧾 Customers")
                st.dataframe(pd.DataFrame(cust, columns=["Name", "Phone", "Service", "Date"]), use_container_width=True)

            # Appointments
            app = fetch_all("SELECT * FROM appointments WHERE cust_name LIKE %s OR emp_id LIKE %s", (like_query, like_query))
            if app:
                st.subheader("📅 Appointments")
                st.dataframe(pd.DataFrame(app, columns=["Customer", "Service", "Employee ID", "Date", "Status"]), use_container_width=True)

            # Billing
            bill = fetch_all("SELECT * FROM billing WHERE cust_name LIKE %s OR service LIKE %s", (like_query, like_query))
            if bill:
                st.subheader("💰 Billing")
                st.dataframe(pd.DataFrame(bill, columns=["Customer", "Service", "Amount", "Date"]), use_container_width=True)

            if not any([emp, cust, app, bill]):
                st.warning("No matches found.")

        except Exception as e:
            st.error(f"Search error: {e}")
    else:
        st.info("Type above to start searching across the entire system.")