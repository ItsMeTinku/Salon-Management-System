"""
attendance.py — Attendance Tracker module
──────────────────────────────────────────────────────────────
KEY CHANGES FROM ORIGINAL:
  1. BUG FIX — False "✅ Attendance recorded successfully!" after
     failed validation:

     Original code:
         if not emp_check:
             st.warning("Note: Employee ID '...' is not in the system yet. Recording anyway.")
         # ← NO return / st.stop() here!
         data = { ... }
         success = supabase_insert("attendance", data)   # ← runs regardless
         if success:
             st.success("✅ Attendance recorded successfully!")   # ← always shown

     The warning was cosmetic — execution continued unconditionally.
     The attendance row was always inserted even for ghost IDs.

     FIX:
       a) Change the warning to st.error() — missing employee is a
          hard error, not an advisory note.
       b) Add st.stop() immediately after, which halts the current
          script execution path so the insert and success message
          are never reached.
       c) Use supabase_exists() (non-cached) so a newly added employee
          is found immediately without waiting for cache expiry.

  2. Duplicate attendance prevention: before inserting, check whether
     a record already exists for (emp_id, date).  Prevents accidental
     double-marking.

  3. All user-facing messages follow error / warning / success
     semantics consistently.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database import supabase_insert, supabase_select, supabase_exists


def attendance_module():
    st.markdown(
        "<h1 style='color: #0f172a;'>📌 Attendance Tracker</h1>",
        unsafe_allow_html=True,
    )
    st.markdown("Record daily attendance for your staff.")

    tabs = st.tabs(["📝 Mark Attendance", "📋 View Records", "📊 Statistics"])

    # ═══════════════════════ MARK ═══════════════════════
    with tabs[0]:
        st.subheader("Daily Attendance")
        with st.container(border=True):
            with st.form("mark_attendance_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    emp_id = st.text_input("Employee ID *")
                    emp_name = st.text_input("Employee Name *")
                with col2:
                    status = st.selectbox(
                        "Status", ["Present", "Absent", "Half Day", "On Leave"]
                    )
                    att_date = st.date_input("Date", value=datetime.now())

                submit = st.form_submit_button(
                    "Submit Attendance", type="primary", use_container_width=True
                )

                if submit:
                    # ── Step 1: Basic field validation ─────────────────
                    if not emp_id.strip() or not emp_name.strip():
                        st.error("❌ Please fill all required fields.")
                        st.stop()   # Halt — nothing below executes

                    # ── Step 2: Employee must exist in the system ──────
                    # WHY supabase_exists() and not supabase_select()?
                    # supabase_select() is @st.cache_data.  If an employee
                    # was added minutes ago, the cached result might still
                    # return an empty list, causing a valid employee to be
                    # rejected.  supabase_exists() always queries live.
                    employee_found = supabase_exists(
                        "employees", {"id": emp_id.strip()}
                    )
                    if not employee_found:
                        # FIX: Hard error + st.stop() so execution halts.
                        # The original code used st.warning() with no stop,
                        # so the insert and success message ran anyway.
                        st.error(
                            f"❌ Employee ID **'{emp_id.strip()}'** does not exist "
                            "in the system. Add the employee in Employee Management "
                            "before recording attendance."
                        )
                        st.stop()   # ← This is the critical missing line

                    # ── Step 3: Prevent duplicate entry for same day ───
                    already_marked = supabase_exists(
                        "attendance",
                        {"emp_id": emp_id.strip(), "date": str(att_date)},
                    )
                    if already_marked:
                        st.warning(
                            f"⚠️ Attendance for Employee **'{emp_id.strip()}'** "
                            f"on **{att_date}** has already been recorded. "
                            "Delete the existing record first if you need to correct it."
                        )
                        st.stop()   # Halt — duplicate insert prevented

                    # ── Step 4: All checks passed — safe to insert ─────
                    data = {
                        "emp_id": emp_id.strip(),
                        "emp_name": emp_name.strip(),
                        "status": status,
                        "date": str(att_date),
                    }
                    success = supabase_insert("attendance", data)
                    if success:
                        st.toast(f"Attendance marked for {emp_name.strip()}", icon="✅")
                        st.success(f"✅ Attendance recorded successfully for '{emp_name.strip()}'!")

    # ═══════════════════════ VIEW ═══════════════════════
    with tabs[1]:
        st.subheader("Attendance Records")
        filter_date = st.date_input("Filter by Date (leave blank for all)", value=None)

        if filter_date:
            data = supabase_select("attendance", match_filter={"date": str(filter_date)})
        else:
            data = supabase_select("attendance")

        if data:
            df = pd.DataFrame(data)
            cols_to_show = [c for c in ["date", "emp_id", "emp_name", "status"] if c in df.columns]
            df = df[cols_to_show]
            df.columns = ["Date", "Employee ID", "Name", "Status"]
            df = df.sort_values(by="Date", ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇ Export Records", csv, "attendance.csv", "text/csv")
        else:
            st.info("No attendance records found.")

    # ═══════════════════════ STATISTICS ═══════════════════════
    with tabs[2]:
        st.subheader("Attendance Statistics")
        data = supabase_select("attendance")
        if data:
            df = pd.DataFrame(data)

            st.markdown("### Overall Status Summary")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("✅ Present",  len(df[df["status"] == "Present"]))
            col2.metric("❌ Absent",   len(df[df["status"] == "Absent"]))
            col3.metric("🕐 Half Day", len(df[df["status"] == "Half Day"]))
            col4.metric("🌴 On Leave", len(df[df["status"] == "On Leave"]))

            st.markdown("### Distribution")
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            st.bar_chart(data=status_counts, x="Status", y="Count")
        else:
            st.info("Not enough data to generate statistics.")
