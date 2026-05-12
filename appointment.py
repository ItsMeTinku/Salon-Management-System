import streamlit as st
import pandas as pd
from datetime import datetime
from database import c, conn

# ================= APPOINTMENT MODULE =================
def appointment_module():

    st.title("📅 Appointment Management")

    # ---------- SUBPAGE CONTROL ----------
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
            "Haircut",
            "Makeup",
            "Facial",
            "Manicure",
            "Pedicure"
        ])

        emp_id = st.text_input("Employee ID")
        date = st.date_input("Appointment Date")

        status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])

        if st.button("Book Appointment", use_container_width=True):

            if cust_name == "" or emp_id == "":
                st.error("Please fill all required fields")
            else:
                c.execute(
                    "INSERT INTO appointments VALUES (?,?,?,?,?)",
                    (cust_name, service, emp_id, str(date), status)
                )
                conn.commit()
                st.success("Appointment Booked Successfully")

    # ================= VIEW APPOINTMENTS =================
    elif action == "View":

        st.subheader("📋 All Appointments")

        data = c.execute("SELECT * FROM appointments").fetchall()

        if data:
            df = pd.DataFrame(
                data,
                columns=["Customer", "Service", "Employee ID", "Date", "Status"]
            )
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No appointments found")

    # ================= SEARCH =================
    elif action == "Search":

        st.subheader("🔍 Search Appointment")

        cust_name = st.text_input("Customer Name")

        if st.button("Search"):

            result = c.execute(
                "SELECT * FROM appointments WHERE cust_name=?",
                (cust_name,)
            ).fetchall()

            if result:
                st.table(result)
            else:
                st.warning("No appointment found")

    # ================= UPDATE =================
    elif action == "Update":

        st.subheader("✏️ Update Appointment")

        cust_name = st.text_input("Customer Name")

        new_service = st.selectbox("New Service", [
            "Haircut",
            "Makeup",
            "Facial",
            "Manicure",
            "Pedicure"
        ])

        new_emp = st.text_input("New Employee ID")
        new_date = st.date_input("New Date")

        new_status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])

        if st.button("Update Appointment"):

            c.execute(
                "UPDATE appointments SET service=?, emp_id=?, date=?, status=? WHERE cust_name=?",
                (new_service, new_emp, str(new_date), new_status, cust_name)
            )
            conn.commit()
            st.success("Appointment Updated Successfully")

    # ================= DELETE =================
    elif action == "Delete":

        st.subheader("🗑️ Delete Appointment")

        cust_name = st.text_input("Customer Name")

        if st.button("Delete Appointment"):

            c.execute(
                "DELETE FROM appointments WHERE cust_name=?",
                (cust_name,)
            )
            conn.commit()

            st.warning("Appointment Deleted")