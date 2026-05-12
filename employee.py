import streamlit as st
import pandas as pd
from database import c, conn

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
            "Hair Stylist",
            "Makeup Artist",
            "Receptionist",
            "Spa Therapist",
            "Nail Technician"
        ])

        salary = st.text_input("Salary")

        if st.button("Add Employee", use_container_width=True):

            if emp_id == "" or name == "":
                st.error("Fill all fields")
            else:
                c.execute(
                    "INSERT INTO employees VALUES (?,?,?,?)",
                    (emp_id, name, profession, salary)
                )
                conn.commit()
                st.success("Employee Added")

    # ================= VIEW =================
    elif action == "View":

        st.subheader("📋 Employee List")

        data = c.execute("SELECT * FROM employees").fetchall()

        if data:
            df = pd.DataFrame(data, columns=["ID","Name","Profession","Salary"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No employees found")

    # ================= SEARCH =================
    elif action == "Search":

        st.subheader("🔍 Search Employee")

        emp_id = st.text_input("Employee ID")

        if st.button("Search"):
            result = c.execute(
                "SELECT * FROM employees WHERE id=?",
                (emp_id,)
            ).fetchall()

            st.table(result if result else [])

    # ================= UPDATE =================
    elif action == "Update":

        st.subheader("✏️ Update Employee")

        emp_id = st.text_input("Employee ID")
        name = st.text_input("New Name")

        profession = st.selectbox("New Profession", [
            "Hair Stylist",
            "Makeup Artist",
            "Receptionist",
            "Spa Therapist",
            "Nail Technician"
        ])

        salary = st.text_input("New Salary")

        if st.button("Update"):
            c.execute(
                "UPDATE employees SET name=?, profession=?, salary=? WHERE id=?",
                (name, profession, salary, emp_id)
            )
            conn.commit()
            st.success("Updated Successfully")

    # ================= DELETE =================
    elif action == "Delete":

        st.subheader("🗑️ Delete Employee")

        emp_id = st.text_input("Employee ID")

        if st.button("Delete"):
            c.execute("DELETE FROM employees WHERE id=?", (emp_id,))
            conn.commit()
            st.warning("Deleted Successfully")