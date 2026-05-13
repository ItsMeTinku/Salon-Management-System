import streamlit as st
import pandas as pd
from datetime import datetime
from database import execute_query, fetch_all

def appointment_module():
    st.title("📅 Appointments")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    action = st.radio(
        "Select Action",
        ["Add", "View", "Search", "Update", "Delete"],
        index=["Add", "View", "Search", "Update", "Delete"].index(st.session_state.subpage),
        key="app_action_radio"
    )
    st.session_state.subpage = action

    if action == "Add":
        st.subheader("➕ Book Appointment")
        with st.form("book_app_form", clear_on_submit=True):
            cust_name = st.text_input("Customer Name")
            service = st.selectbox("Service", ["Haircut", "Makeup", "Facial", "Manicure", "Pedicure"])
            emp_id = st.text_input("Employee ID")
            date = st.date_input("Date", min_value=datetime.now())
            status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
            
            submit = st.form_submit_button("Book Now", use_container_width=True)
            if submit:
                if not cust_name.strip() or not emp_id.strip():
                    st.error("Please fill all fields")
                else:
                    success = execute_query(
                        "INSERT INTO appointments (cust_name, service, emp_id, date, status) VALUES (%s, %s, %s, %s, %s)",
                        (cust_name.strip(), service, emp_id.strip(), str(date), status)
                    )
                    if success:
                        st.success(f"✅ Appointment booked for '{cust_name}'!")

    elif action == "View":
        st.subheader("📋 Schedule")
        data = fetch_all("SELECT * FROM appointments")
        if data:
            df = pd.DataFrame(data, columns=["Customer", "Service", "Employee ID", "Date", "Status"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No appointments found.")

    elif action == "Update":
        st.subheader("✏️ Update Status")
        with st.form("update_app_form"):
            cust_search = st.text_input("Customer Name to Update")
            new_status = st.selectbox("New Status", ["Pending", "Completed", "Cancelled"])
            
            update_submit = st.form_submit_button("Update Status", use_container_width=True)
            if update_submit:
                success = execute_query(
                    "UPDATE appointments SET status=%s WHERE cust_name=%s",
                    (new_status, cust_search.strip())
                )
                if success:
                    st.success("✅ Status updated!")

    elif action == "Delete":
        st.subheader("🗑️ Cancel Appointment")
        cust_del = st.text_input("Customer Name to Delete")
        if st.button("Delete Appointment", use_container_width=True):
            success = execute_query("DELETE FROM appointments WHERE cust_name=%s", (cust_del.strip(),))
            if success:
                st.warning("🗑️ Appointment removed.")