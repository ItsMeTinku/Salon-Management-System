"""
billing.py — Billing & Invoices module
──────────────────────────────────────────────────────────────
KEY CHANGES FROM ORIGINAL:
  1. BUG FIX — "st.download_button() can't be used in an st.form()":
     Streamlit forbids download_button inside a form because forms
     batch widget state and submit via a single button; a download
     button would fire immediately on click, conflicting with form
     submission semantics.

     FIX PATTERN:
       a) On form submit: generate the PDF and store the raw bytes
          in st.session_state["invoice_pdf_bytes"] along with the
          file name.  Do NOT call st.download_button here.
       b) After the form block (outside the `with st.form` and even
          outside the `with st.container`): check session_state and
          render the download button if bytes are present.

     This is the canonical Streamlit pattern for post-form downloads.

  2. Invoice PDF bytes are stored (not just the file path) so the
     download works on Streamlit Cloud where /tmp may be ephemeral
     between re-runs.

  3. A "Clear Invoice" button lets the user dismiss the download
     widget once they no longer need it.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
from database import supabase_insert, supabase_select, supabase_delete
from invoice import generate_invoice


def billing_module():
    st.markdown("<h1 style='color: #0f172a;'>💰 Billing & Invoices</h1>", unsafe_allow_html=True)
    st.markdown("Generate invoices and track revenue.")

    # Initialise session state keys used by the download widget
    if "invoice_pdf_bytes" not in st.session_state:
        st.session_state.invoice_pdf_bytes = None
    if "invoice_file_name" not in st.session_state:
        st.session_state.invoice_file_name = None

    tabs = st.tabs(["🧾 Create Invoice", "📋 Billing History", "🗑️ Delete Record"])

    # ═══════════════════════ CREATE ═══════════════════════
    with tabs[0]:
        st.subheader("Generate New Invoice")
        with st.container(border=True):
            # ── The form collects data and triggers PDF generation ──
            with st.form("billing_form", clear_on_submit=False):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Customer Name *")
                    service = st.selectbox(
                        "Service",
                        ["Haircut", "Makeup", "Facial", "Manicure",
                         "Pedicure", "Hair Coloring", "Spa", "Package"],
                    )
                with col2:
                    amount = st.number_input("Amount (₹)", min_value=0, step=100)
                    discount = st.number_input(
                        "Discount (%)", min_value=0, max_value=100, value=0
                    )

                submit = st.form_submit_button(
                    "Generate & Save Bill", type="primary", use_container_width=True
                )

                if submit:
                    if not name.strip() or amount <= 0:
                        st.error("❌ Enter a valid customer name and amount greater than 0.")
                        # Clear any stale invoice from previous runs
                        st.session_state.invoice_pdf_bytes = None
                        st.session_state.invoice_file_name = None
                    else:
                        final_amount = amount - (amount * (discount / 100))

                        data = {
                            "cust_name": name.strip(),
                            "service": service,
                            "amount": final_amount,
                        }
                        success = supabase_insert("billing", data)

                        if success:
                            st.toast("Invoice generated!", icon="✅")
                            st.success(
                                f"✅ Invoice saved for '{name.strip()}' "
                                f"— Total ₹{final_amount:.2f}"
                            )

                            # ── Generate PDF and store bytes in session_state ──
                            # WHY: We cannot call st.download_button here inside
                            # the form.  Instead we persist the PDF bytes so the
                            # download button rendered BELOW the form can serve
                            # them on the very next Streamlit re-run.
                            try:
                                pdf_path = generate_invoice(
                                    name.strip(), service, final_amount
                                )
                                with open(pdf_path, "rb") as f:
                                    st.session_state.invoice_pdf_bytes = f.read()
                                st.session_state.invoice_file_name = (
                                    f"{name.strip()}_invoice.pdf"
                                )
                            except Exception as e:
                                st.error(f"❌ PDF generation failed: {e}")
                                st.session_state.invoice_pdf_bytes = None

        # ── Download button lives OUTSIDE the form ──────────────────
        # WHY outside: Streamlit explicitly prohibits st.download_button
        # inside st.form (raises StreamlitAPIException).  This block is
        # still inside `tabs[0]` so it appears in the correct tab, but
        # it is no longer nested inside `with st.form(...)`.
        if st.session_state.invoice_pdf_bytes is not None:
            st.divider()
            col_dl, col_clear = st.columns([3, 1])
            with col_dl:
                st.download_button(
                    label="📄 Download PDF Invoice",
                    data=st.session_state.invoice_pdf_bytes,
                    file_name=st.session_state.invoice_file_name,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                )
            with col_clear:
                if st.button("✖ Clear", use_container_width=True):
                    # Reset so the button disappears after the user is done
                    st.session_state.invoice_pdf_bytes = None
                    st.session_state.invoice_file_name = None
                    st.rerun()

    # ═══════════════════════ HISTORY ═══════════════════════
    with tabs[1]:
        st.subheader("Billing History")
        data = supabase_select("billing")
        if data:
            df = pd.DataFrame(data)
            cols_to_show = [c for c in ["date", "cust_name", "service", "amount"] if c in df.columns]
            df = df[cols_to_show]
            df.columns = ["Date", "Customer", "Service", "Amount (₹)"]
            df = df.sort_values(by="Date", ascending=False)

            st.dataframe(df, use_container_width=True, hide_index=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇ Export Revenue Data", csv, "billing_history.csv", "text/csv"
            )
        else:
            st.info("No billing records found.")

    # ═══════════════════════ DELETE ═══════════════════════
    with tabs[2]:
        st.subheader("Delete Invoice Record")
        with st.container(border=True):
            st.warning(
                "⚠️ Deleting an invoice affects your revenue analytics. Proceed with caution."
            )
            name_del = st.text_input("Customer Name to Delete Records For")
            if st.button("Delete Records", type="primary"):
                if not name_del.strip():
                    st.error("❌ Please enter a customer name.")
                else:
                    existing = supabase_select("billing", match_filter={"cust_name": name_del.strip()})
                    if existing:
                        success = supabase_delete("billing", {"cust_name": name_del.strip()})
                        if success:
                            st.toast("Record deleted.", icon="🗑️")
                            st.success("🗑️ Billing records deleted successfully.")
                    else:
                        st.error("❌ No billing records found for this customer.")
