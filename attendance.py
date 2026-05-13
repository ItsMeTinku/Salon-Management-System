import streamlit as st
import pandas as pd
from datetime import datetime
from database import execute_query, fetch_all

def attendance_module():
    st.title("📌 Attendance")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Mark"

    action = st.radio(
        "Select Action",
        ["Mark", "View", "Report"],
        index=["Mark", "View", "Report"].index(st.session_state.subpage),
        key="att_action_radio"
    )
    st.session_state.subpage = action

    if action == "Mark":
        st.subheader("📝 Mark Daily Attendance")
        with st.form("mark_attendance_form", clear_on_submit=True):
            emp_id = st.text_input("Employee ID")
            emp_name = st.text_input("Employee Name")
            status = st.selectbox("Status", ["Present", "Absent", "Half Day"])
            date = datetime.now().strftime("%Y-%m-%d")
            
            st.write(f"Date: **{date}**")
            submit = st.form_submit_button("Submit Attendance", use_container_width=True)
            
            if submit:
                if not emp_id.strip() or not emp_name.strip():
                    st.error("Please fill all fields")
                else:
                    success = execute_query(
                        "INSERT INTO attendance (emp_id, emp_name, status, date) VALUES (%s, %s, %s, %s)",
                        (emp_id.strip(), emp_name.strip(), status, date)
                    )
                    if success:
                        st.success(f"✅ Attendance marked for {emp_name}!")

    elif action == "View":
        st.subheader("📋 Records")
        data = fetch_all("SELECT * FROM attendance")
        if data:
            df = pd.DataFrame(data, columns=["Employee ID", "Name", "Status", "Date"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No records.")

    elif action == "Report":
        st.subheader("📊 Statistics")
        data = fetch_all("SELECT emp_name, status FROM attendance")
        if data:
            df = pd.DataFrame(data, columns=["Employee", "Status"])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("✅ Present", len(df[df["Status"] == "Present"]))
            col2.metric("❌ Absent", len(df[df["Status"] == "Absent"]))
            col3.metric("🕐 Half Day", len(df[df["Status"] == "Half Day"]))
            
            st.bar_chart(df["Status"].value_counts())
        else:
            st.info("No data.")