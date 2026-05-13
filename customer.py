import streamlit as st
import pandas as pd
from datetime import datetime
from database import execute_query, fetch_all

def customer_module():
    st.title("🧾 Customer Management")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    action = st.radio(
        "Select Action",
        ["Add", "View", "Search", "Delete"],
        index=["Add", "View", "Search", "Delete"].index(st.session_state.subpage),
        key="cust_action_radio"
    )
    st.session_state.subpage = action

    if action == "Add":
        st.subheader("➕ Add New Customer")
        with st.form("add_customer_form", clear_on_submit=True):
            name = st.text_input("Customer Name")
            phone = st.text_input("Phone Number")
            service = st.selectbox("Service", ["Haircut", "Makeup", "Facial", "Manicure", "Pedicure"])
            
            submit = st.form_submit_button("Save Customer", use_container_width=True)
            if submit:
                if not name.strip() or not phone.strip():
                    st.error("Please fill all fields")
                else:
                    success = execute_query(
                        "INSERT INTO customers (cust_name, phone, service, visit_date) VALUES (%s, %s, %s, %s)",
                        (name.strip(), phone.strip(), service, str(datetime.now().date()))
                    )
                    if success:
                        st.success(f"✅ Customer '{name}' added!")

    elif action == "View":
        st.subheader("📋 All Customers")
        data = fetch_all("SELECT * FROM customers")
        if data:
            df = pd.DataFrame(data, columns=["Name", "Phone", "Service", "Date"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No customers found.")

    elif action == "Search":
        st.subheader("🔍 Search Customer")
        phone_search = st.text_input("Enter Phone Number")
        if st.button("Search", use_container_width=True):
            result = fetch_all("SELECT * FROM customers WHERE phone=%s", (phone_search.strip(),))
            if result:
                df = pd.DataFrame(result, columns=["Name", "Phone", "Service", "Date"])
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No customer found.")

    elif action == "Delete":
        st.subheader("🗑️ Delete Customer")
        phone_del = st.text_input("Enter Phone to Delete")
        if st.button("Delete Customer", use_container_width=True):
            if not phone_del.strip():
                st.error("Enter phone number")
            else:
                success = execute_query("DELETE FROM customers WHERE phone=%s", (phone_del.strip(),))
                if success:
                    st.warning("🗑️ Customer deleted.")