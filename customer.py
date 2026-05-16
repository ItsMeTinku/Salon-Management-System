"""
customer.py — Customer CRM module
──────────────────────────────────────────────────────────────
KEY CHANGES FROM ORIGINAL:
  1. BUG FIX — RLS Insert Error (42501):
     Before inserting, we call supabase_exists() (the non-cached
     helper) to check whether the phone number already exists.
     This prevents a duplicate-key insert AND gives a clear
     "already exists" message instead of a cryptic DB error.

  2. BUG FIX — Existing customers not fetched correctly:
     supabase_select() is @st.cache_data.  If the user just added
     a customer and immediately views the directory, the cache
     still holds the old list.  We call clear_db_cache() explicitly
     before re-rendering the directory tab so the list is always
     fresh after any mutation.

  3. Added phone-number format validation before any DB call so
     bad data never reaches Supabase.

  4. All error paths use st.error(); success paths use st.toast +
     st.success for visual consistency.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database import (
    supabase_insert,
    supabase_select,
    supabase_delete,
    supabase_exists,
    clear_db_cache,
)


def customer_module():
    st.markdown("<h1 style='color: #0f172a;'>🧾 Customer CRM</h1>", unsafe_allow_html=True)
    st.markdown("Manage customer profiles and view their service history.")

    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    tabs = st.tabs(["➕ Add New", "📋 Directory", "🔍 Search", "🗑️ Delete"])

    # ═══════════════════════ ADD ═══════════════════════
    with tabs[0]:
        st.subheader("New Customer Profile")
        with st.container(border=True):
            with st.form("add_customer_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Customer Name *")
                    phone = st.text_input("Phone Number *")
                with col2:
                    service = st.selectbox(
                        "Preferred Service",
                        ["Haircut", "Makeup", "Facial", "Manicure",
                         "Pedicure", "Hair Coloring", "Spa"],
                    )
                    date = st.date_input("Initial Visit Date", max_value=datetime.now())

                submit = st.form_submit_button(
                    "Save Customer Profile", type="primary", use_container_width=True
                )

                if submit:
                    # ── Client-side validation ──────────────────────────
                    name_clean = name.strip()
                    phone_clean = phone.strip()

                    if not name_clean or not phone_clean:
                        st.error("❌ Please provide both Name and Phone Number.")
                        st.stop()

                    if not phone_clean.isdigit() or len(phone_clean) < 7:
                        st.error("❌ Phone number must be digits only (min 7 digits).")
                        st.stop()

                    # ── Duplicate check (bypasses cache) ────────────────
                    # WHY: supabase_exists() queries Supabase directly.
                    # If we used supabase_select() here the cached result
                    # might not reflect a customer added 30 seconds ago.
                    already_exists = supabase_exists("customers", {"phone": phone_clean})
                    if already_exists:
                        st.warning(
                            f"⚠️ A customer with phone **{phone_clean}** already exists. "
                            "Use the Search tab to view their profile."
                        )
                        st.stop()

                    # ── Insert ──────────────────────────────────────────
                    data = {
                        "phone": phone_clean,
                        "cust_name": name_clean,
                        "service": service,
                        "visit_date": str(date),
                    }
                    success = supabase_insert("customers", data)
                    if success:
                        st.toast(f"Profile for {name_clean} created!", icon="✅")
                        st.success(f"✅ Customer '{name_clean}' added successfully!")

    # ═══════════════════════ VIEW ═══════════════════════
    with tabs[1]:
        st.subheader("Customer Directory")

        # Force-refresh after any mutation so the directory is never stale.
        # WHY: clear_db_cache() was called inside supabase_insert/delete,
        # but Streamlit re-runs happen before the next cache miss is
        # registered.  Calling it here ensures this tab always reads live.
        clear_db_cache()
        data = supabase_select("customers")

        if data:
            df = pd.DataFrame(data)
            cols_to_show = [c for c in ["cust_name", "phone", "service", "visit_date"] if c in df.columns]
            df = df[cols_to_show]
            df.columns = ["Name", "Phone", "Service", "Visit Date"]

            st.dataframe(df, use_container_width=True, hide_index=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇ Export Directory (CSV)", csv, "customers.csv", "text/csv")
        else:
            st.info("No customers found in the CRM.")

    # ═══════════════════════ SEARCH ═══════════════════════
    with tabs[2]:
        st.subheader("Search Customer")
        with st.container(border=True):
            phone_search = st.text_input("Enter Phone Number or Name")
            if st.button("Search", type="primary"):
                if not phone_search.strip():
                    st.info("Please enter a search term.")
                else:
                    # Use OR filter so a partial name OR phone matches
                    filter_str = (
                        f"phone.ilike.%{phone_search.strip()}%,"
                        f"cust_name.ilike.%{phone_search.strip()}%"
                    )
                    result = supabase_select("customers", or_filter=filter_str)

                    if result:
                        df = pd.DataFrame(result)
                        cols_to_show = [
                            c for c in ["cust_name", "phone", "service", "visit_date"]
                            if c in df.columns
                        ]
                        df_show = df[cols_to_show]
                        df_show.columns = ["Name", "Phone", "Service", "Visit Date"]
                        st.dataframe(df_show, use_container_width=True, hide_index=True)

                        st.markdown("### Recent Billing Activity")
                        cust_name = result[0].get("cust_name")
                        bills = supabase_select("billing", match_filter={"cust_name": cust_name})
                        if bills:
                            b_df = pd.DataFrame(bills)
                            b_cols = [c for c in ["date", "service", "amount"] if c in b_df.columns]
                            st.dataframe(b_df[b_cols], use_container_width=True, hide_index=True)
                        else:
                            st.write("No billing history found.")
                    else:
                        st.warning("No customer found matching that criteria.")

    # ═══════════════════════ DELETE ═══════════════════════
    with tabs[3]:
        st.subheader("Delete Customer")
        with st.container(border=True):
            phone_del = st.text_input("Enter Phone Number to Delete")
            if st.button("Delete Customer Profile", type="primary"):
                if not phone_del.strip():
                    st.error("❌ Enter a phone number.")
                else:
                    # WHY supabase_exists() and not supabase_select() here?
                    # After a recent insert the cached select might still
                    # return [] for this phone, making it look like the
                    # customer doesn't exist even though they do.
                    exists = supabase_exists("customers", {"phone": phone_del.strip()})
                    if exists:
                        success = supabase_delete("customers", {"phone": phone_del.strip()})
                        if success:
                            st.toast("Customer deleted.", icon="🗑️")
                            st.warning("🗑️ Customer profile removed successfully.")
                    else:
                        st.error("❌ Phone number not found in database.")
