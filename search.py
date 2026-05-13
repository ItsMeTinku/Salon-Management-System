import streamlit as st
import pandas as pd
from database import c, PH

# ═══════════════════════════════════════════════
# GLOBAL SEARCH MODULE
# ═══════════════════════════════════════════════
def global_search():

    st.title("🔍 Global Search System")

    query = st.text_input("Search anything (Employee / Customer / Appointment / Billing)")

    if st.button("Search", use_container_width=True):

        if not query.strip():
            st.warning("Please enter a search term.")
            return

        like = f"%{query.strip()}%"

        try:
            st.subheader("👩‍💼 Employees")
            emp = c.execute(
                f"SELECT * FROM employees WHERE name LIKE {PH} OR id LIKE {PH}",
                (like, like)
            ).fetchall()
            if emp:
                st.dataframe(pd.DataFrame(emp, columns=["ID", "Name", "Profession", "Salary"]), use_container_width=True)
            else:
                st.info("No employees found.")

            st.subheader("🧾 Customers")
            cust = c.execute(
                f"SELECT * FROM customers WHERE cust_name LIKE {PH} OR phone LIKE {PH}",
                (like, like)
            ).fetchall()
            if cust:
                st.dataframe(pd.DataFrame(cust, columns=["Name", "Phone", "Service", "Date"]), use_container_width=True)
            else:
                st.info("No customers found.")

            st.subheader("📅 Appointments")
            app = c.execute(
                f"SELECT * FROM appointments WHERE cust_name LIKE {PH} OR emp_id LIKE {PH}",
                (like, like)
            ).fetchall()
            if app:
                st.dataframe(pd.DataFrame(app, columns=["Customer", "Service", "Employee ID", "Date", "Status"]), use_container_width=True)
            else:
                st.info("No appointments found.")

            st.subheader("💰 Billing")
            bill = c.execute(
                f"SELECT * FROM billing WHERE cust_name LIKE {PH} OR service LIKE {PH}",
                (like, like)
            ).fetchall()
            if bill:
                st.dataframe(pd.DataFrame(bill, columns=["Customer", "Service", "Amount", "Date"]), use_container_width=True)
            else:
                st.info("No billing records found.")

        except Exception as e:
            st.error(f"❌ Search error: {e}")