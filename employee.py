import streamlit as st
import pandas as pd
import sqlite3
from database import c, conn, PH

# ─── catch IntegrityError for both backends ───
try:
    import psycopg2
    _INTEGRITY_ERRORS = (sqlite3.IntegrityError, psycopg2.IntegrityError)
except ImportError:
    _INTEGRITY_ERRORS = (sqlite3.IntegrityError,)

def employee_module():

    st.title("👩‍💼 Employee Management")

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

        st.subheader("➕ Add Employee")

        emp_id     = st.text_input("Employee ID")
        name       = st.text_input("Name")
        profession = st.selectbox("Profession", [
            "Hair Stylist", "Makeup Artist", "Receptionist",
            "Spa Therapist", "Nail Technician"
        ])
        salary = st.text_input("Salary")

        if st.button("Add Employee", use_container_width=True):
            if not emp_id.strip() or not name.strip() or not salary.strip():
                st.error("Please fill all fields.")
            else:
                try:
                    c.execute(
                        f"INSERT INTO employees VALUES ({PH},{PH},{PH},{PH})",
                        (emp_id.strip(), name.strip(), profession, salary.strip())
                    )
                    conn.commit()
                    st.success(f"✅ Employee '{name}' added successfully!")
                except _INTEGRITY_ERRORS:
                    conn.rollback()
                    st.error(f"❌ Employee ID '{emp_id}' already exists. Use a unique ID.")
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Error saving employee: {e}")

    # ═══════════════════ VIEW ══════════════════
    elif action == "View":

        st.subheader("📋 Employee List")
        try:
            data = c.execute("SELECT * FROM employees").fetchall()
            if data:
                df = pd.DataFrame(data, columns=["ID", "Name", "Profession", "Salary"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No employees found. Add employees first.")
        except Exception as e:
            st.error(f"❌ Error loading employees: {e}")

    # ═══════════════════ SEARCH ════════════════
    elif action == "Search":

        st.subheader("🔍 Search Employee")
        emp_id = st.text_input("Employee ID")

        if st.button("Search", use_container_width=True):
            try:
                result = c.execute(
                    f"SELECT * FROM employees WHERE id={PH}",
                    (emp_id.strip(),)
                ).fetchall()
                if result:
                    df = pd.DataFrame(result, columns=["ID", "Name", "Profession", "Salary"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No employee found with that ID.")
            except Exception as e:
                st.error(f"❌ Search error: {e}")

    # ═══════════════════ UPDATE ════════════════
    elif action == "Update":

        st.subheader("✏️ Update Employee")
        emp_id     = st.text_input("Employee ID to Update")
        name       = st.text_input("New Name")
        profession = st.selectbox("New Profession", [
            "Hair Stylist", "Makeup Artist", "Receptionist",
            "Spa Therapist", "Nail Technician"
        ])
        salary = st.text_input("New Salary")

        if st.button("Update", use_container_width=True):
            if not emp_id.strip():
                st.error("Please enter the Employee ID to update.")
            else:
                try:
                    c.execute(
                        f"UPDATE employees SET name={PH}, profession={PH}, salary={PH} WHERE id={PH}",
                        (name.strip(), profession, salary.strip(), emp_id.strip())
                    )
                    conn.commit()
                    if c.rowcount == 0:
                        st.warning("No employee found with that ID.")
                    else:
                        st.success("✅ Employee updated successfully!")
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Update error: {e}")

    # ═══════════════════ DELETE ════════════════
    elif action == "Delete":

        st.subheader("🗑️ Delete Employee")
        emp_id = st.text_input("Employee ID to Delete")

        if st.button("Delete", use_container_width=True):
            if not emp_id.strip():
                st.error("Please enter an Employee ID.")
            else:
                try:
                    c.execute(
                        f"DELETE FROM employees WHERE id={PH}",
                        (emp_id.strip(),)
                    )
                    conn.commit()
                    if c.rowcount == 0:
                        st.warning("No employee found with that ID.")
                    else:
                        st.warning(f"🗑️ Employee '{emp_id}' deleted successfully.")
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Delete error: {e}")