import streamlit as st
import pandas as pd
from datetime import datetime
from database import c, conn, PH

# ═══════════════════════════════════════════════
# APPOINTMENT MODULE
# ═══════════════════════════════════════════════
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

    # ═══════════════════ ADD ═══════════════════
    if action == "Add":

        st.subheader("➕ Book Appointment")

        cust_name = st.text_input("Customer Name")
        service   = st.selectbox("Service", [
            "Haircut", "Makeup", "Facial", "Manicure", "Pedicure"
        ])
        emp_id = st.text_input("Employee ID")
        date   = st.date_input("Appointment Date")
        status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])

        if st.button("Book Appointment", use_container_width=True):
            if not cust_name.strip() or not emp_id.strip():
                st.error("Please fill all required fields.")
            else:
                try:
                    c.execute(
                        f"INSERT INTO appointments VALUES ({PH},{PH},{PH},{PH},{PH})",
                        (cust_name.strip(), service, emp_id.strip(), str(date), status)
                    )
                    conn.commit()
                    st.success(f"✅ Appointment booked for '{cust_name}' on {date}!")
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Error booking appointment: {e}")

    # ═══════════════════ VIEW ══════════════════
    elif action == "View":

        st.subheader("📋 All Appointments")
        try:
            data = c.execute("SELECT * FROM appointments").fetchall()
            if data:
                df = pd.DataFrame(data, columns=["Customer", "Service", "Employee ID", "Date", "Status"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No appointments found.")
        except Exception as e:
            st.error(f"❌ Error loading appointments: {e}")

    # ═══════════════════ SEARCH ════════════════
    elif action == "Search":

        st.subheader("🔍 Search Appointment")
        cust_name = st.text_input("Customer Name")

        if st.button("Search", use_container_width=True):
            try:
                result = c.execute(
                    f"SELECT * FROM appointments WHERE cust_name={PH}",
                    (cust_name.strip(),)
                ).fetchall()
                if result:
                    df = pd.DataFrame(result, columns=["Customer", "Service", "Employee ID", "Date", "Status"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No appointment found for that customer.")
            except Exception as e:
                st.error(f"❌ Search error: {e}")

    # ═══════════════════ UPDATE ════════════════
    elif action == "Update":

        st.subheader("✏️ Update Appointment")
        cust_name   = st.text_input("Customer Name")
        new_service = st.selectbox("New Service", [
            "Haircut", "Makeup", "Facial", "Manicure", "Pedicure"
        ])
        new_emp    = st.text_input("New Employee ID")
        new_date   = st.date_input("New Date")
        new_status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])

        if st.button("Update Appointment", use_container_width=True):
            if not cust_name.strip():
                st.error("Please enter the customer name.")
            else:
                try:
                    c.execute(
                        f"UPDATE appointments SET service={PH}, emp_id={PH}, date={PH}, status={PH} WHERE cust_name={PH}",
                        (new_service, new_emp.strip(), str(new_date), new_status, cust_name.strip())
                    )
                    conn.commit()
                    if c.rowcount == 0:
                        st.warning("No appointment found for that customer.")
                    else:
                        st.success("✅ Appointment updated successfully!")
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Update error: {e}")

    # ═══════════════════ DELETE ════════════════
    elif action == "Delete":

        st.subheader("🗑️ Delete Appointment")
        cust_name = st.text_input("Customer Name")

        if st.button("Delete Appointment", use_container_width=True):
            if not cust_name.strip():
                st.error("Please enter the customer name.")
            else:
                try:
                    c.execute(
                        f"DELETE FROM appointments WHERE cust_name={PH}",
                        (cust_name.strip(),)
                    )
                    conn.commit()
                    if c.rowcount == 0:
                        st.warning("No appointment found for that customer.")
                    else:
                        st.warning(f"🗑️ Appointment for '{cust_name}' deleted.")
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Delete error: {e}")