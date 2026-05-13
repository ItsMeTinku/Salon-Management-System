import streamlit as st
import pandas as pd
from database import execute_query, fetch_all

def employee_module():
    st.title("👩‍💼 Employee Management")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    # Use session state for the radio to prevent reset
    action = st.radio(
        "Select Action",
        ["Add", "View", "Search", "Update", "Delete"],
        index=["Add","View","Search","Update","Delete"].index(st.session_state.subpage),
        key="emp_action_radio"
    )
    st.session_state.subpage = action

    # ================= ADD (FORM OPTIMIZED) =================
    if action == "Add":
        st.subheader("➕ Add Employee")
        
        with st.form("add_employee_form", clear_on_submit=True):
            emp_id = st.text_input("Employee ID")
            name = st.text_input("Name")
            profession = st.selectbox("Profession", [
                "Hair Stylist", "Makeup Artist", "Receptionist",
                "Spa Therapist", "Nail Technician"
            ])
            salary = st.text_input("Salary")
            
            submit = st.form_submit_button("Add Employee", use_container_width=True)
            
            if submit:
                if not emp_id.strip() or not name.strip() or not salary.strip():
                    st.error("Please fill all fields")
                else:
                    success = execute_query(
                        "INSERT INTO employees (id, name, profession, salary) VALUES (%s, %s, %s, %s)",
                        (emp_id.strip(), name.strip(), profession, salary.strip())
                    )
                    if success:
                        st.success(f"✅ Employee '{name}' added successfully!")

    # ================= VIEW (CACHED) =================
    elif action == "View":
        st.subheader("📋 Employee List")
        # This uses cached fetch_all from database.py
        data = fetch_all("SELECT * FROM employees")
        if data:
            df = pd.DataFrame(data, columns=["ID", "Name", "Profession", "Salary"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No employees found.")

    # ================= SEARCH =================
    elif action == "Search":
        st.subheader("🔍 Search Employee")
        emp_id_search = st.text_input("Enter Employee ID")

        if st.button("Search", use_container_width=True):
            result = fetch_all("SELECT * FROM employees WHERE id=%s", (emp_id_search.strip(),))
            if result:
                df = pd.DataFrame(result, columns=["ID", "Name", "Profession", "Salary"])
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No employee found with that ID.")

    # ================= UPDATE =================
    elif action == "Update":
        st.subheader("✏️ Update Employee")
        with st.form("update_employee_form"):
            emp_id_up = st.text_input("Employee ID to Update")
            name_up = st.text_input("New Name")
            profession_up = st.selectbox("New Profession", [
                "Hair Stylist", "Makeup Artist", "Receptionist",
                "Spa Therapist", "Nail Technician"
            ])
            salary_up = st.text_input("New Salary")
            
            update_submit = st.form_submit_button("Update Details", use_container_width=True)
            
            if update_submit:
                if not emp_id_up.strip():
                    st.error("Employee ID is required")
                else:
                    success = execute_query(
                        "UPDATE employees SET name=%s, profession=%s, salary=%s WHERE id=%s",
                        (name_up.strip(), profession_up, salary_up.strip(), emp_id_up.strip())
                    )
                    if success:
                        st.success("✅ Employee updated successfully!")

    # ================= DELETE =================
    elif action == "Delete":
        st.subheader("🗑️ Delete Employee")
        emp_id_del = st.text_input("Employee ID to Delete")

        if st.button("Confirm Delete", use_container_width=True):
            if not emp_id_del.strip():
                st.error("Please enter an ID.")
            else:
                success = execute_query("DELETE FROM employees WHERE id=%s", (emp_id_del.strip(),))
                if success:
                    st.warning(f"🗑️ Employee '{emp_id_del}' deleted.")