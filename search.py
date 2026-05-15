import streamlit as st
import pandas as pd
from database import supabase_select

def global_search():
    st.markdown("<h1 style='color: #0f172a;'>🔍 Global Search</h1>", unsafe_allow_html=True)
    st.markdown("Search across all modules: Employees, Customers, Appointments, and Billing.")

    with st.container(border=True):
        query = st.text_input("Enter search term (Name, Phone, ID, Service...)", key="global_search_input")

        if query.strip():
            st.markdown("---")
            search_term = query.strip()
            found_any = False
            
            try:
                # 1. Search Employees (name, id, profession)
                emp_filter = f"name.ilike.%{search_term}%,id.ilike.%{search_term}%,profession.ilike.%{search_term}%"
                emp = supabase_select("employees", or_filter=emp_filter)
                if emp:
                    found_any = True
                    st.markdown("### 👩‍💼 Employees")
                    df = pd.DataFrame(emp)
                    cols = [c for c in ["id", "name", "profession", "salary"] if c in df.columns]
                    st.dataframe(df[cols], use_container_width=True, hide_index=True)

                # 2. Search Customers (cust_name, phone, service)
                cust_filter = f"cust_name.ilike.%{search_term}%,phone.ilike.%{search_term}%,service.ilike.%{search_term}%"
                cust = supabase_select("customers", or_filter=cust_filter)
                if cust:
                    found_any = True
                    st.markdown("### 🧾 Customers")
                    df = pd.DataFrame(cust)
                    cols = [c for c in ["cust_name", "phone", "service", "visit_date"] if c in df.columns]
                    st.dataframe(df[cols], use_container_width=True, hide_index=True)

                # 3. Search Appointments (cust_name, emp_id, service, status)
                app_filter = f"cust_name.ilike.%{search_term}%,emp_id.ilike.%{search_term}%,service.ilike.%{search_term}%,status.ilike.%{search_term}%"
                app = supabase_select("appointments", or_filter=app_filter)
                if app:
                    found_any = True
                    st.markdown("### 📅 Appointments")
                    df = pd.DataFrame(app)
                    cols = [c for c in ["date", "cust_name", "service", "emp_id", "status"] if c in df.columns]
                    st.dataframe(df[cols], use_container_width=True, hide_index=True)

                # 4. Search Billing (cust_name, service)
                bill_filter = f"cust_name.ilike.%{search_term}%,service.ilike.%{search_term}%"
                bill = supabase_select("billing", or_filter=bill_filter)
                if bill:
                    found_any = True
                    st.markdown("### 💰 Billing")
                    df = pd.DataFrame(bill)
                    cols = [c for c in ["date", "cust_name", "service", "amount"] if c in df.columns]
                    st.dataframe(df[cols], use_container_width=True, hide_index=True)

                if not found_any:
                    st.warning(f"No matches found for '{search_term}' anywhere in the system.")

            except Exception as e:
                st.error(f"Search error: {e}")
        else:
            st.info("Start typing above to search the database.")