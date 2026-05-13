import streamlit as st
import pandas as pd
from datetime import datetime
from database import c, conn, PH

# ═══════════════════════════════════════════════
# ATTENDANCE MODULE
# ═══════════════════════════════════════════════
def attendance_module():

    st.title("📌 Employee Attendance System")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Mark"

    action = st.radio(
        "Select Action",
        ["Mark", "View", "Report"],
        index=["Mark", "View", "Report"].index(st.session_state.subpage)
    )
    st.session_state.subpage = action

    # ═══════════════════ MARK ══════════════════
    if action == "Mark":

        st.subheader("📝 Mark Attendance")

        emp_id   = st.text_input("Employee ID")
        emp_name = st.text_input("Employee Name")
        status   = st.selectbox("Status", ["Present", "Absent", "Half Day"])
        date     = datetime.now().strftime("%Y-%m-%d")

        st.info(f"📅 Today's date: **{date}**")

        if st.button("Submit Attendance", use_container_width=True):
            if not emp_id.strip() or not emp_name.strip():
                st.error("Please fill all fields.")
            else:
                try:
                    c.execute(
                        f"INSERT INTO attendance VALUES ({PH},{PH},{PH},{PH})",
                        (emp_id.strip(), emp_name.strip(), status, date)
                    )
                    conn.commit()
                    st.success(f"✅ Attendance marked: {emp_name} — {status} on {date}")
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Error marking attendance: {e}")

    # ═══════════════════ VIEW ══════════════════
    elif action == "View":

        st.subheader("📋 Attendance Records")
        try:
            data = c.execute("SELECT * FROM attendance").fetchall()
            if data:
                df = pd.DataFrame(data, columns=["Employee ID", "Name", "Status", "Date"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No attendance records yet.")
        except Exception as e:
            st.error(f"❌ Error loading attendance: {e}")

    # ═══════════════════ REPORT ════════════════
    elif action == "Report":

        st.subheader("📊 Attendance Report")
        try:
            data = c.execute("SELECT emp_name, status FROM attendance").fetchall()
            if data:
                df = pd.DataFrame(data, columns=["Employee", "Status"])

                present  = len(df[df["Status"] == "Present"])
                absent   = len(df[df["Status"] == "Absent"])
                half_day = len(df[df["Status"] == "Half Day"])

                col1, col2, col3 = st.columns(3)
                col1.metric("✅ Present",  present)
                col2.metric("❌ Absent",   absent)
                col3.metric("🕐 Half Day", half_day)

                st.bar_chart(df["Status"].value_counts())
            else:
                st.info("No attendance data available.")
        except Exception as e:
            st.error(f"❌ Error generating report: {e}")