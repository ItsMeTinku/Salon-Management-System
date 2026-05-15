import streamlit as st
import pandas as pd
from datetime import datetime
import os
from database import supabase_insert, supabase_select, supabase_delete
from invoice import generate_invoice

def billing_module():
    st.markdown("<h1 style='color: #0f172a;'>💰 Billing & Invoices</h1>", unsafe_allow_html=True)
    st.markdown("Generate invoices and track revenue.")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    tabs = st.tabs(["🧾 Create Invoice", "📋 Billing History", "🗑️ Delete Record"])

    # ================= CREATE =================
    with tabs[0]:
        st.subheader("Generate New Invoice")
        with st.container(border=True):
            with st.form("billing_form", clear_on_submit=False):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Customer Name *")
                    service = st.selectbox("Service", [
                        "Haircut", "Makeup", "Facial", "Manicure", 
                        "Pedicure", "Hair Coloring", "Spa", "Package"
                    ])
                with col2:
                    amount = st.number_input("Amount (₹)", min_value=0, step=100)
                    discount = st.number_input("Discount (%)", min_value=0, max_value=100, value=0)
                    
                submit = st.form_submit_button("Generate & Save Bill", type="primary", use_container_width=True)
                
                if submit:
                    if not name.strip() or amount <= 0:
                        st.error("Enter valid customer name and amount.")
                    else:
                        final_amount = amount - (amount * (discount / 100))
                        
                        data = {
                            "cust_name": name.strip(),
                            "service": service,
                            "amount": final_amount,
                            # Supabase will auto-populate 'date' if defined in schema, but we can set it explicitly
                        }
                        
                        success = supabase_insert("billing", data)
                        if success:
                            st.toast("Invoice generated!", icon="✅")
                            st.success(f"✅ Invoice saved for '{name}' with total ₹{final_amount:.2f}")
                            
                            # Generate PDF
                            try:
                                pdf_path = generate_invoice(name.strip(), service, final_amount)
                                with open(pdf_path, "rb") as f:
                                    st.download_button(
                                        "📄 Download PDF Invoice",
                                        f,
                                        file_name=os.path.basename(pdf_path),
                                        mime="application/pdf",
                                        type="primary"
                                    )
                            except Exception as e:
                                st.error(f"Invoice PDF generation failed: {e}")

    # ================= HISTORY =================
    with tabs[1]:
        st.subheader("Billing History")
        data = supabase_select("billing")
        if data:
            df = pd.DataFrame(data)
            cols_to_show = ["date", "cust_name", "service", "amount"]
            cols_to_show = [c for c in cols_to_show if c in df.columns]
            df = df[cols_to_show]
            df.columns = ["Date", "Customer", "Service", "Amount (₹)"]
            
            # Sort by newest
            df = df.sort_values(by="Date", ascending=False)
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇ Export Revenue Data", csv, "billing_history.csv", "text/csv")
        else:
            st.info("No billing records found.")

    # ================= DELETE =================
    with tabs[2]:
        st.subheader("Delete Invoice Record")
        with st.container(border=True):
            st.warning("Deleting an invoice affects your revenue analytics. Proceed with caution.")
            name_del = st.text_input("Customer Name to Delete Records For")
            if st.button("Delete Records", type="primary"):
                if name_del.strip():
                    existing = supabase_select("billing", match_filter={"cust_name": name_del.strip()})
                    if existing:
                        success = supabase_delete("billing", {"cust_name": name_del.strip()})
                        if success:
                            st.toast("Record deleted.", icon="🗑️")
                            st.success("🗑️ Billing records deleted successfully.")
                    else:
                        st.error("No billing records found for this customer.")
                else:
                    st.error("Please enter a customer name.")