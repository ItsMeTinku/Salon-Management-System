import streamlit as st
import pandas as pd
from datetime import datetime
import os
from database import c, conn, PH
from invoice import generate_invoice

# ═══════════════════════════════════════════════
# BILLING MODULE
# ═══════════════════════════════════════════════
def billing_module():

    st.title("💰 Billing System (ERP Level)")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    action = st.radio(
        "Select Action",
        ["Add", "View", "Search", "Delete"],
        index=["Add", "View", "Search", "Delete"].index(st.session_state.subpage)
    )
    st.session_state.subpage = action

    # ═══════════════════ ADD ═══════════════════
    if action == "Add":

        st.subheader("🧾 Generate Invoice")

        name    = st.text_input("Customer Name")
        service = st.selectbox("Service", [
            "Haircut", "Makeup", "Facial", "Manicure", "Pedicure"
        ])
        amount = st.number_input("Amount (₹)", min_value=0)

        if st.button("Generate Bill", use_container_width=True):
            if not name.strip():
                st.error("Please enter the customer name.")
            else:
                try:
                    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    c.execute(
                        f"INSERT INTO billing VALUES ({PH},{PH},{PH},{PH})",
                        (name.strip(), service, str(amount), date)
                    )
                    conn.commit()

                    # Generate PDF invoice
                    pdf_file = generate_invoice(name.strip(), service, amount)
                    st.success(f"✅ Invoice generated for '{name}'!")

                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            "📄 Download Invoice PDF",
                            f,
                            file_name=os.path.basename(pdf_file),
                            mime="application/pdf"
                        )
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Error generating bill: {e}")

    # ═══════════════════ VIEW ══════════════════
    elif action == "View":

        st.subheader("📋 All Bills")
        try:
            data = c.execute("SELECT * FROM billing").fetchall()
            if data:
                df = pd.DataFrame(data, columns=["Customer", "Service", "Amount", "Date"])
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇ Export CSV", csv, "billing_report.csv", "text/csv")
            else:
                st.info("No billing records found.")
        except Exception as e:
            st.error(f"❌ Error loading billing data: {e}")

    # ═══════════════════ SEARCH ════════════════
    elif action == "Search":

        st.subheader("🔍 Search Bill")
        name = st.text_input("Customer Name")

        if st.button("Search", use_container_width=True):
            try:
                result = c.execute(
                    f"SELECT * FROM billing WHERE cust_name LIKE {PH}",
                    (f"%{name.strip()}%",)
                ).fetchall()
                if result:
                    df = pd.DataFrame(result, columns=["Customer", "Service", "Amount", "Date"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No billing records found for that customer.")
            except Exception as e:
                st.error(f"❌ Search error: {e}")

    # ═══════════════════ DELETE ════════════════
    elif action == "Delete":

        st.subheader("🗑️ Delete Bill")
        name = st.text_input("Customer Name to Delete")

        if st.button("Delete Bill", use_container_width=True):
            if not name.strip():
                st.error("Please enter the customer name.")
            else:
                try:
                    c.execute(
                        f"DELETE FROM billing WHERE cust_name={PH}",
                        (name.strip(),)
                    )
                    conn.commit()
                    if c.rowcount == 0:
                        st.warning("No billing record found for that customer.")
                    else:
                        st.warning(f"🗑️ Billing record for '{name}' deleted.")
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Delete error: {e}")