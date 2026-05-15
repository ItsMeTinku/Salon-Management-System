import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import supabase_insert, supabase_select, supabase_update, supabase_delete

def appointment_module():
    st.markdown("<h1 style='color: #0f172a;'>📅 Appointments</h1>", unsafe_allow_html=True)
    st.markdown("Schedule and manage customer appointments.")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    tabs = st.tabs(["➕ Book", "📋 Schedule", "🔍 Search", "✏️ Update Status", "🗑️ Cancel"])

    # ================= BOOK =================
    with tabs[0]:
        st.subheader("Book Appointment")
        with st.container(border=True):
            with st.form("book_app_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    cust_name = st.text_input("Customer Name *")
                    emp_id = st.text_input("Assigned Employee ID *")
                with col2:
                    service = st.selectbox("Service", [
                        "Haircut", "Makeup", "Facial", "Manicure", 
                        "Pedicure", "Hair Coloring", "Spa"
                    ])
                    app_date = st.date_input("Date", min_value=datetime.now())
                
                status = st.selectbox("Status", ["Pending", "Confirmed", "Completed", "Cancelled"])
                
                submit = st.form_submit_button("Book Now", type="primary", use_container_width=True)
                
                if submit:
                    if not cust_name.strip() or not emp_id.strip():
                        st.error("Please fill all required fields.")
                    else:
                        # Check if Employee exists
                        emp_check = supabase_select("employees", match_filter={"id": emp_id.strip()})
                        if not emp_check:
                            st.error(f"Employee ID '{emp_id}' does not exist.")
                        else:
                            data = {
                                "cust_name": cust_name.strip(),
                                "service": service,
                                "emp_id": emp_id.strip(),
                                "date": str(app_date),
                                "status": status
                            }
                            success = supabase_insert("appointments", data)
                            if success:
                                st.toast(f"Appointment booked for {cust_name}!", icon="✅")
                                st.success(f"✅ Appointment booked successfully!")

    # ================= SCHEDULE =================
    with tabs[1]:
        st.subheader("Appointment Schedule")
        
        # Add filter
        filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Confirmed", "Completed", "Cancelled"])
        
        if filter_status == "All":
            data = supabase_select("appointments")
        else:
            data = supabase_select("appointments", match_filter={"status": filter_status})
            
        if data:
            df = pd.DataFrame(data)
            cols_to_show = ["date", "cust_name", "service", "emp_id", "status"]
            cols_to_show = [c for c in cols_to_show if c in df.columns]
            df = df[cols_to_show]
            df.columns = ["Date", "Customer", "Service", "Employee ID", "Status"]
            
            # Sort by date
            df = df.sort_values(by="Date", ascending=False)
            
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No appointments found for this filter.")

    # ================= SEARCH =================
    with tabs[2]:
        st.subheader("Search Appointments")
        with st.container(border=True):
            search_query = st.text_input("Search by Customer Name")
            if st.button("Search", type="primary", key="search_app"):
                if search_query.strip():
                    result = supabase_select("appointments", ilike_filter={"cust_name": search_query.strip()})
                    if result:
                        df = pd.DataFrame(result)
                        cols = [c for c in ["date", "cust_name", "service", "status"] if c in df.columns]
                        df_show = df[cols]
                        st.dataframe(df_show, use_container_width=True, hide_index=True)
                    else:
                        st.warning("No appointments found.")
                else:
                    st.info("Enter a search term.")

    # ================= UPDATE =================
    with tabs[3]:
        st.subheader("Update Appointment Status")
        with st.container(border=True):
            st.write("Find an appointment by Customer Name and Date.")
            up_cust = st.text_input("Customer Name (exact match)")
            if up_cust:
                apps = supabase_select("appointments", match_filter={"cust_name": up_cust.strip()})
                if apps:
                    # Let user pick which appointment to update if there are multiple
                    app_options = {f"{a['date']} - {a['service']} ({a['status']})": a['id'] for a in apps if 'id' in a}
                    if app_options:
                        selected_app = st.selectbox("Select Appointment", list(app_options.keys()))
                        app_id = app_options[selected_app]
                        
                        with st.form("update_app_form"):
                            new_status = st.selectbox("New Status", ["Pending", "Confirmed", "Completed", "Cancelled"])
                            
                            update_submit = st.form_submit_button("Update Status", type="primary", use_container_width=True)
                            if update_submit:
                                success = supabase_update("appointments", {"status": new_status}, {"id": app_id})
                                if success:
                                    st.toast("Status updated!", icon="✅")
                                    st.success("✅ Appointment status updated successfully!")
                    else:
                        st.warning("Could not identify appointment ID. Make sure schema has an 'id' UUID.")
                else:
                    st.warning("No appointments found for this customer.")

    # ================= DELETE =================
    with tabs[4]:
        st.subheader("Cancel/Remove Appointment")
        with st.container(border=True):
            del_cust = st.text_input("Customer Name to Delete")
            if st.button("Delete Appointments", type="primary"):
                if del_cust.strip():
                    existing = supabase_select("appointments", match_filter={"cust_name": del_cust.strip()})
                    if existing:
                        success = supabase_delete("appointments", {"cust_name": del_cust.strip()})
                        if success:
                            st.toast("Appointments removed.", icon="🗑️")
                            st.warning("🗑️ All matching appointments deleted.")
                    else:
                        st.error("No appointments found for this customer.")
                else:
                    st.error("Please enter a customer name.")