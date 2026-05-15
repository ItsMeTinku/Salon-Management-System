import streamlit as st
import pandas as pd
from datetime import datetime
from database import supabase_insert, supabase_select, supabase_delete

def customer_module():
    st.markdown("<h1 style='color: #0f172a;'>🧾 Customer CRM</h1>", unsafe_allow_html=True)
    st.markdown("Manage customer profiles and view their service history.")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    tabs = st.tabs(["➕ Add New", "📋 Directory", "🔍 Search", "🗑️ Delete"])

    # ================= ADD =================
    with tabs[0]:
        st.subheader("New Customer Profile")
        with st.container(border=True):
            with st.form("add_customer_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Customer Name *")
                    phone = st.text_input("Phone Number *")
                with col2:
                    service = st.selectbox("Preferred Service", [
                        "Haircut", "Makeup", "Facial", "Manicure", 
                        "Pedicure", "Hair Coloring", "Spa"
                    ])
                    date = st.date_input("Initial Visit Date", max_value=datetime.now())
                
                submit = st.form_submit_button("Save Customer Profile", type="primary", use_container_width=True)
                
                if submit:
                    if not name.strip() or not phone.strip():
                        st.error("Please provide both Name and Phone Number.")
                    else:
                        data = {
                            "phone": phone.strip(),
                            "cust_name": name.strip(),
                            "service": service,
                            "visit_date": str(date)
                        }
                        success = supabase_insert("customers", data)
                        if success:
                            st.toast(f"Profile for {name} created!", icon="✅")
                            st.success(f"✅ Customer '{name}' added successfully!")

    # ================= VIEW =================
    with tabs[1]:
        st.subheader("Customer Directory")
        data = supabase_select("customers")
        if data:
            df = pd.DataFrame(data)
            cols_to_show = ["cust_name", "phone", "service", "visit_date"]
            cols_to_show = [c for c in cols_to_show if c in df.columns]
            df = df[cols_to_show]
            df.columns = ["Name", "Phone", "Service", "Visit Date"]
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇ Export Directory (CSV)", csv, "customers.csv", "text/csv")
        else:
            st.info("No customers found in the CRM.")

    # ================= SEARCH =================
    with tabs[2]:
        st.subheader("Search Customer")
        with st.container(border=True):
            phone_search = st.text_input("Enter Phone Number or Name")
            if st.button("Search", type="primary"):
                if phone_search.strip():
                    filter_str = f"phone.ilike.%{phone_search.strip()}%,cust_name.ilike.%{phone_search.strip()}%"
                    result = supabase_select("customers", or_filter=filter_str)
                    
                    if result:
                        df = pd.DataFrame(result)
                        cols_to_show = [c for c in ["cust_name", "phone", "service", "visit_date"] if c in df.columns]
                        df_show = df[cols_to_show]
                        df_show.columns = ["Name", "Phone", "Service", "Visit Date"]
                        st.dataframe(df_show, use_container_width=True, hide_index=True)
                        
                        # Show customer history (if we had a specific view for appointments/billing)
                        st.markdown("### Recent Activity")
                        cust_name = result[0].get("cust_name")
                        bills = supabase_select("billing", match_filter={"cust_name": cust_name})
                        if bills:
                            st.write("Billing History:")
                            b_df = pd.DataFrame(bills)[["date", "service", "amount"]]
                            st.dataframe(b_df, use_container_width=True, hide_index=True)
                        else:
                            st.write("No billing history found.")
                    else:
                        st.warning("No customer found matching that criteria.")
                else:
                    st.info("Please enter search criteria.")

    # ================= DELETE =================
    with tabs[3]:
        st.subheader("Delete Customer")
        with st.container(border=True):
            phone_del = st.text_input("Enter Phone Number to Delete")
            if st.button("Delete Customer Profile", type="primary"):
                if not phone_del.strip():
                    st.error("Enter phone number.")
                else:
                    existing = supabase_select("customers", match_filter={"phone": phone_del.strip()})
                    if existing and len(existing) > 0:
                        success = supabase_delete("customers", {"phone": phone_del.strip()})
                        if success:
                            st.toast("Customer deleted.", icon="🗑️")
                            st.warning("🗑️ Customer profile removed successfully.")
                    else:
                        st.error("Phone number not found in database.")