import streamlit as st
import pandas as pd
from datetime import datetime
from database import c, conn

# ================= ATTENDANCE MODULE =================
def attendance_module():

    st.title("📌 Employee Attendance System")

    # ---------- SUBPAGE ----------
    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Mark"

    action = st.radio(
        "Select Action",
        ["Mark", "View", "Report"],
        index=["Mark", "View", "Report"].index(st.session_state.subpage)
    )

    st.session_state.subpage = action

    # ================= MARK ATTENDANCE =================
    if action == "Mark":

        st.subheader("📝 Mark Attendance")

        emp_id = st.text_input("Employee ID")
        emp_name = st.text_input("Employee Name")

        status = st.selectbox("Status", ["Present", "Absent", "Half Day"])

        date = datetime.now().strftime("%Y-%m-%d")

        if st.button("Submit Attendance", use_container_width=True):

            if emp_id == "" or emp_name == "":
                st.error("Please fill all fields")
            else:
                c.execute(
                    "INSERT INTO attendance VALUES (?,?,?,?)",
                    (emp_id, emp_name, status, date)
                )
                conn.commit()
                st.success("Attendance Marked")

    # ================= VIEW ATTENDANCE =================
    elif action == "View":

        st.subheader("📋 Attendance Records")

        data = c.execute("SELECT * FROM attendance").fetchall()

        if data:
            df = pd.DataFrame(
                data,
                columns=["Employee ID", "Name", "Status", "Date"]
            )
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No attendance records")

    # ================= REPORT =================
    elif action == "Report":

        st.subheader("📊 Attendance Report")

        data = c.execute("SELECT emp_name, status FROM attendance").fetchall()

        if data:
            df = pd.DataFrame(data, columns=["Employee", "Status"])

            present = len(df[df["Status"] == "Present"])
            absent = len(df[df["Status"] == "Absent"])

            st.metric("Present", present)
            st.metric("Absent", absent)

            st.bar_chart(df["Status"].value_counts())
        else:
            st.info("No data available")