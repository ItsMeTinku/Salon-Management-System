import streamlit as st
import pandas as pd
from datetime import datetime
import os
from database import execute_query, fetch_all
from invoice import generate_invoice

def billing_module():
    st.title("💰 Billing & Invoices")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    action = st.radio(
        "Select Action",
        ["Add", "View", "Search", "Delete"],
        index=["Add","View","Search","Delete"].index(st.session_state.subpage),
        key="bill_action_radio"
    )
    st.session_state.subpage = action

    if action == "Add":
        st.subheader("🧾 Create Invoice")
        with st.form("billing_form", clear_on_submit=False):
            name = st.text_input("Customer Name")
            service = st.selectbox("Service", ["Haircut", "Makeup", "Facial", "Manicure", "Pedicure"])
            amount = st.number_input("Amount (₹)", min_value=0)
            
            submit = st.form_submit_button("Generate & Save Bill", use_container_width=True)
            if submit:
                if not name.strip():
                    st.error("Enter customer name")
                else:
                    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    success = execute_query(
                        "INSERT INTO billing (cust_name, service, amount, date) VALUES (%s, %s, %s, %s)",
                        (name.strip(), service, str(amount), date)
                    )
                    if success:
                        pdf_path = generate_invoice(name.strip(), service, amount)
                        st.success(f"✅ Invoice saved for '{name}'!")
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                "📄 Download PDF",
                                f,
                                file_name=os.path.basename(pdf_path),
                                mime="application/pdf"
                            )

    elif action == "View":
        st.subheader("📋 Billing History")
        data = fetch_all("SELECT * FROM billing")
        if data:
            df = pd.DataFrame(data, columns=["Customer", "Service", "Amount", "Date"])
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇ Export CSV", csv, "billing.csv", "text/csv")
        else:
            st.info("No records.")

    elif action == "Delete":
        st.subheader("🗑️ Delete Invoice Record")
        name_del = st.text_input("Customer Name to Delete")
        if st.button("Delete Record", use_container_width=True):
            success = execute_query("DELETE FROM billing WHERE cust_name=%s", (name_del.strip(),))
            if success:
                st.warning(f"🗑️ Record deleted.")