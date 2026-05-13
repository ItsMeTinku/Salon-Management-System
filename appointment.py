import streamlit as st
import pandas as pd
from datetime import datetime
from database import execute_query, fetch_all

def appointment_module():
    st.title("📅 Appointment Management")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    action = st.radio(
        "Select Action",
        ["Add", "View", "Search", "Update", "Delete"],
        index=["Add", "View", "Search", "Update", "Delete"].index(st.session_state.subpage)
    )
    st.session_state.subpage = action

    # ================= ADD APPOINTMENT =================
    if action == "Add":
        st.subheader("➕ Book Appointment")
        cust_name = st.text_input("Customer Name")
        service = st.selectbox("Service", [
            "Haircut", "Makeup", "Facial", "Manicure", "Pedicure"
        ])
        emp_id = st.text_input("Employee ID")
        date = st.date_input("Appointment Date")
        status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])

        if st.button("Book Appointment", use_container_width=True):
            if not cust_name.strip() or not emp_id.strip():
                st.error("Please fill all required fields")
            else:
                success = execute_query(
                    "INSERT INTO appointments (cust_name, service, emp_id, date, status) VALUES (%s, %s, %s, %s, %s)",
                    (cust_name.strip(), service, emp_id.strip(), str(date), status)
                )
                if success:
                    st.success(f"✅ Appointment booked for '{cust_name}'!")

    # ================= VIEW APPOINTMENTS =================
    elif action == "View":
        st.subheader("📋 All Appointments")
        data = fetch_all("SELECT * FROM appointments")
        if data:
            df = pd.DataFrame(data, columns=["Customer", "Service", "Employee ID", "Date", "Status"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No appointments found.")

    # ================= SEARCH =================
    elif action == "Search":
        st.subheader("🔍 Search Appointment")
        cust_name = st.text_input("Customer Name")

        if st.button("Search", use_container_width=True):
            result = fetch_all("SELECT * FROM appointments WHERE cust_name=%s", (cust_name.strip(),))
            if result:
                df = pd.DataFrame(result, columns=["Customer", "Service", "Employee ID", "Date", "Status"])
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No appointment found for that customer.")

    # ================= UPDATE =================
    elif action == "Update":
        st.subheader("✏️ Update Appointment")
        cust_name = st.text_input("Customer Name")
        new_service = st.selectbox("New Service", ["Haircut", "Makeup", "Facial", "Manicure", "Pedicure"])
        new_emp = st.text_input("New Employee ID")
        new_date = st.date_input("New Date")
        new_status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])

        if st.button("Update Appointment", use_container_width=True):
            if not cust_name.strip():
                st.error("Please enter the customer name.")
            else:
                success = execute_query(
                    "UPDATE appointments SET service=%s, emp_id=%s, date=%s, status=%s WHERE cust_name=%s",
                    (new_service, new_emp.strip(), str(new_date), new_status, cust_name.strip())
                )
                if success:
                    st.success("✅ Appointment updated successfully!")

    # ================= DELETE =================
    elif action == "Delete":
        st.subheader("🗑️ Delete Appointment")
        cust_name = st.text_input("Customer Name")

        if st.button("Delete Appointment", use_container_width=True):
            if not cust_name.strip():
                st.error("Please enter the customer name.")
            else:
                success = execute_query("DELETE FROM appointments WHERE cust_name=%s", (cust_name.strip(),))
                if success:
                    st.warning("🗑️ Appointment deleted.")