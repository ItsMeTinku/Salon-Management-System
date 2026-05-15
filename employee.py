import streamlit as st
import pandas as pd
from database import supabase_insert, supabase_select, supabase_update, supabase_delete
from datetime import datetime

def employee_module():
    st.markdown("<h1 style='color: #0f172a;'>👩‍💼 Employee Management</h1>", unsafe_allow_html=True)
    st.markdown("Manage your salon staff, track professions, and update salaries.")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    # Use horizontal radio buttons or tabs for a more modern look
    tabs = st.tabs(["➕ Add", "📋 View All", "🔍 Search", "✏️ Update", "🗑️ Delete"])

    # ================= ADD =================
    with tabs[0]:
        st.subheader("Add New Employee")
        with st.container(border=True):
            with st.form("add_employee_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    emp_id = st.text_input("Employee ID *")
                    name = st.text_input("Full Name *")
                with col2:
                    profession = st.selectbox("Profession", [
                        "Hair Stylist", "Makeup Artist", "Receptionist",
                        "Spa Therapist", "Nail Technician", "Manager"
                    ])
                    salary = st.number_input("Salary (₹)", min_value=0, step=1000)
                
                submit = st.form_submit_button("Add Employee", type="primary", use_container_width=True)
                
                if submit:
                    if not emp_id.strip() or not name.strip() or salary <= 0:
                        st.error("Please fill all required fields correctly.")
                    else:
                        data = {
                            "id": emp_id.strip(),
                            "name": name.strip(),
                            "profession": profession,
                            "salary": str(salary)
                        }
                        success = supabase_insert("employees", data)
                        if success:
                            st.toast(f"Employee '{name}' added!", icon="✅")
                            st.success(f"✅ Employee '{name}' added successfully!")

    # ================= VIEW =================
    with tabs[1]:
        st.subheader("Employee Roster")
        data = supabase_select("employees")
        if data:
            df = pd.DataFrame(data)
            # Reorder columns for better UI
            cols_to_show = ["id", "name", "profession", "salary", "created_at"]
            # only select columns that exist
            cols_to_show = [c for c in cols_to_show if c in df.columns]
            df = df[cols_to_show]
            df.columns = [c.replace("_", " ").title() for c in df.columns]
            
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No employees found. Start by adding one.")

    # ================= SEARCH =================
    with tabs[2]:
        st.subheader("Search Employee")
        with st.container(border=True):
            emp_search = st.text_input("Search by Name or ID")
            if st.button("Search", type="primary"):
                if emp_search.strip():
                    # We use an OR filter for name and id
                    filter_str = f"name.ilike.%{emp_search.strip()}%,id.ilike.%{emp_search.strip()}%"
                    result = supabase_select("employees", or_filter=filter_str)
                    
                    if result:
                        df = pd.DataFrame(result)
                        cols_to_show = [c for c in ["id", "name", "profession", "salary"] if c in df.columns]
                        st.dataframe(df[cols_to_show], use_container_width=True, hide_index=True)
                    else:
                        st.warning("No employee found matching that search.")
                else:
                    st.info("Please enter a search term.")

    # ================= UPDATE =================
    with tabs[3]:
        st.subheader("Update Employee Details")
        
        # We can make it interactive by first searching the employee
        emp_id_up = st.text_input("Enter Employee ID to Update")
        
        if emp_id_up:
            existing = supabase_select("employees", match_filter={"id": emp_id_up.strip()})
            if existing and len(existing) > 0:
                emp_data = existing[0]
                with st.container(border=True):
                    with st.form("update_employee_form"):
                        name_up = st.text_input("Name", value=emp_data.get("name", ""))
                        
                        prof_index = 0
                        prof_list = ["Hair Stylist", "Makeup Artist", "Receptionist", "Spa Therapist", "Nail Technician", "Manager"]
                        if emp_data.get("profession") in prof_list:
                            prof_index = prof_list.index(emp_data.get("profession"))
                            
                        profession_up = st.selectbox("Profession", prof_list, index=prof_index)
                        
                        # Handle potential string salary
                        try:
                            sal_val = int(float(emp_data.get("salary", 0)))
                        except:
                            sal_val = 0
                            
                        salary_up = st.number_input("Salary (₹)", min_value=0, value=sal_val, step=1000)
                        
                        update_submit = st.form_submit_button("Update Details", type="primary", use_container_width=True)
                        
                        if update_submit:
                            update_data = {
                                "name": name_up.strip(),
                                "profession": profession_up,
                                "salary": str(salary_up)
                            }
                            success = supabase_update("employees", update_data, {"id": emp_id_up.strip()})
                            if success:
                                st.toast("Employee updated successfully!", icon="✅")
                                st.success("✅ Employee updated successfully!")
            else:
                st.warning("Employee ID not found.")

    # ================= DELETE =================
    with tabs[4]:
        st.subheader("Remove Employee")
        with st.container(border=True):
            emp_id_del = st.text_input("Enter Employee ID to Delete")
            if st.button("Confirm Delete", type="primary"):
                if not emp_id_del.strip():
                    st.error("Please enter an ID.")
                else:
                    # Check if exists
                    existing = supabase_select("employees", match_filter={"id": emp_id_del.strip()})
                    if existing and len(existing) > 0:
                        success = supabase_delete("employees", {"id": emp_id_del.strip()})
                        if success:
                            st.toast(f"Employee {emp_id_del} deleted.", icon="🗑️")
                            st.warning(f"🗑️ Employee '{emp_id_del}' deleted.")
                    else:
                        st.error("Employee ID not found.")