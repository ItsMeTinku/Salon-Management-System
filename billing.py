import streamlit as st
import pandas as pd
from datetime import datetime
import os
from database import execute_query, fetch_all
from invoice import generate_invoice

def billing_module():
    st.title("💰 Billing System (ERP Level)")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    action = st.radio(
        "Select Action",
        ["Add", "View", "Search", "Delete"],
        index=["Add","View","Search","Delete"].index(st.session_state.subpage)
    )
    st.session_state.subpage = action

    # ================= ADD BILL =================
    if action == "Add":
        st.subheader("🧾 Generate Invoice")
        name = st.text_input("Customer Name")
        service = st.selectbox("Service", ["Haircut", "Makeup", "Facial", "Manicure", "Pedicure"])
        amount = st.number_input("Amount (₹)", min_value=0)

        if st.button("Generate Bill", use_container_width=True):
            if not name.strip():
                st.error("Please enter the customer name.")
            else:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Using explicit column names and %s placeholders
                success = execute_query(
                    "INSERT INTO billing (cust_name, service, amount, date) VALUES (%s, %s, %s, %s)",
                    (name.strip(), service, str(amount), date)
                )
                if success:
                    pdf_file = generate_invoice(name.strip(), service, amount)
                    st.success(f"✅ Invoice generated for '{name}'!")
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            "📄 Download Invoice PDF",
                            f,
                            file_name=os.path.basename(pdf_file),
                            mime="application/pdf"
                        )

    # ================= VIEW =================
    elif action == "View":
        st.subheader("📋 All Bills")
        data = fetch_all("SELECT * FROM billing")
        if data:
            df = pd.DataFrame(data, columns=["Customer", "Service", "Amount", "Date"])
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇ Export CSV", csv, "billing_report.csv", "text/csv")
        else:
            st.info("No billing records found.")

    # ================= SEARCH =================
    elif action == "Search":
        st.subheader("🔍 Search Bill")
        name = st.text_input("Customer Name")

        if st.button("Search", use_container_width=True):
            result = fetch_all("SELECT * FROM billing WHERE cust_name LIKE %s", (f"%{name.strip()}%",))
            if result:
                df = pd.DataFrame(result, columns=["Customer", "Service", "Amount", "Date"])
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No billing records found for that customer.")

    # ================= DELETE =================
    elif action == "Delete":
        st.subheader("🗑️ Delete Bill")
        name = st.text_input("Customer Name to Delete")

        if st.button("Delete Bill", use_container_width=True):
            if not name.strip():
                st.error("Please enter the customer name.")
            else:
                success = execute_query("DELETE FROM billing WHERE cust_name=%s", (name.strip(),))
                if success:
                    st.warning(f"🗑️ Billing record for '{name}' deleted.")