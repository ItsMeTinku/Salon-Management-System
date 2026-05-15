import streamlit as st
import pandas as pd
from datetime import datetime
from database import supabase_insert, supabase_select

def attendance_module():
    st.markdown("<h1 style='color: #0f172a;'>📌 Attendance Tracker</h1>", unsafe_allow_html=True)
    st.markdown("Record daily attendance for your staff.")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Mark"

    tabs = st.tabs(["📝 Mark Attendance", "📋 View Records", "📊 Statistics"])

    # ================= MARK =================
    with tabs[0]:
        st.subheader("Daily Attendance")
        with st.container(border=True):
            with st.form("mark_attendance_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    emp_id = st.text_input("Employee ID *")
                    emp_name = st.text_input("Employee Name *")
                with col2:
                    status = st.selectbox("Status", ["Present", "Absent", "Half Day", "On Leave"])
                    date = st.date_input("Date", value=datetime.now())
                
                submit = st.form_submit_button("Submit Attendance", type="primary", use_container_width=True)
                
                if submit:
                    if not emp_id.strip() or not emp_name.strip():
                        st.error("Please fill all required fields.")
                    else:
                        # Optional: Validate emp_id against employees table
                        emp_check = supabase_select("employees", match_filter={"id": emp_id.strip()})
                        if not emp_check:
                            st.warning(f"Note: Employee ID '{emp_id}' is not in the system yet. Recording anyway.")
                        
                        data = {
                            "emp_id": emp_id.strip(),
                            "emp_name": emp_name.strip(),
                            "status": status,
                            "date": str(date)
                        }
                        success = supabase_insert("attendance", data)
                        if success:
                            st.toast(f"Attendance marked for {emp_name}", icon="✅")
                            st.success(f"✅ Attendance recorded successfully!")

    # ================= VIEW =================
    with tabs[1]:
        st.subheader("Attendance Records")
        
        # Add date filter
        filter_date = st.date_input("Filter by Date", value=None)
        
        if filter_date:
            data = supabase_select("attendance", match_filter={"date": str(filter_date)})
        else:
            data = supabase_select("attendance")
            
        if data:
            df = pd.DataFrame(data)
            cols_to_show = ["date", "emp_id", "emp_name", "status"]
            cols_to_show = [c for c in cols_to_show if c in df.columns]
            df = df[cols_to_show]
            df.columns = ["Date", "Employee ID", "Name", "Status"]
            
            df = df.sort_values(by="Date", ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇ Export Records", csv, "attendance.csv", "text/csv")
        else:
            st.info("No attendance records found.")

    # ================= REPORT =================
    with tabs[2]:
        st.subheader("Attendance Statistics")
        data = supabase_select("attendance")
        if data:
            df = pd.DataFrame(data)
            
            # KPI Metrics
            st.markdown("### Overall Status Summary")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("✅ Present", len(df[df["status"] == "Present"]))
            col2.metric("❌ Absent", len(df[df["status"] == "Absent"]))
            col3.metric("🕐 Half Day", len(df[df["status"] == "Half Day"]))
            col4.metric("🌴 On Leave", len(df[df["status"] == "On Leave"]))
            
            # Chart
            st.markdown("### Distribution")
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            st.bar_chart(data=status_counts, x="Status", y="Count")
            
        else:
            st.info("Not enough data to generate statistics.")