import streamlit as st
import pandas as pd
from database import execute_query, fetch_all, fetch_one

def employee_module():
    st.title("👩‍💼 Employee Management")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    action = st.radio(
        "Select Action",
        ["Add", "View", "Search", "Update", "Delete"],
        index=["Add","View","Search","Update","Delete"].index(st.session_state.subpage)
    )
    st.session_state.subpage = action

    # ================= ADD =================
    if action == "Add":
        st.subheader("➕ Add Employee")

        emp_id = st.text_input("Employee ID")
        name = st.text_input("Name")
        profession = st.selectbox("Profession", [
            "Hair Stylist", "Makeup Artist", "Receptionist",
            "Spa Therapist", "Nail Technician"
        ])
        salary = st.text_input("Salary")

        if st.button("Add Employee", use_container_width=True):
            if not emp_id.strip() or not name.strip() or not salary.strip():
                st.error("Please fill all fields")
            else:
                # Using explicit column names and %s placeholders
                success = execute_query(
                    "INSERT INTO employees (id, name, profession, salary) VALUES (%s, %s, %s, %s)",
                    (emp_id.strip(), name.strip(), profession, salary.strip())
                )
                if success:
                    st.success(f"✅ Employee '{name}' added successfully!")

    # ================= VIEW =================
    elif action == "View":
        st.subheader("📋 Employee List")
        data = fetch_all("SELECT * FROM employees")
        if data:
            df = pd.DataFrame(data, columns=["ID", "Name", "Profession", "Salary"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No employees found.")

    # ================= SEARCH =================
    elif action == "Search":
        st.subheader("🔍 Search Employee")
        emp_id = st.text_input("Employee ID")

        if st.button("Search", use_container_width=True):
            result = fetch_all("SELECT * FROM employees WHERE id=%s", (emp_id.strip(),))
            if result:
                df = pd.DataFrame(result, columns=["ID", "Name", "Profession", "Salary"])
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No employee found with that ID.")

    # ================= UPDATE =================
    elif action == "Update":
        st.subheader("✏️ Update Employee")
        emp_id = st.text_input("Employee ID to Update")
        name = st.text_input("New Name")
        profession = st.selectbox("New Profession", [
            "Hair Stylist", "Makeup Artist", "Receptionist",
            "Spa Therapist", "Nail Technician"
        ])
        salary = st.text_input("New Salary")

        if st.button("Update", use_container_width=True):
            if not emp_id.strip():
                st.error("Please enter the Employee ID to update.")
            else:
                success = execute_query(
                    "UPDATE employees SET name=%s, profession=%s, salary=%s WHERE id=%s",
                    (name.strip(), profession, salary.strip(), emp_id.strip())
                )
                if success:
                    st.success("✅ Employee updated successfully!")

    # ================= DELETE =================
    elif action == "Delete":
        st.subheader("🗑️ Delete Employee")
        emp_id = st.text_input("Employee ID to Delete")

        if st.button("Delete", use_container_width=True):
            if not emp_id.strip():
                st.error("Please enter an Employee ID.")
            else:
                success = execute_query("DELETE FROM employees WHERE id=%s", (emp_id.strip(),))
                if success:
                    st.warning(f"🗑️ Employee '{emp_id}' deleted.")