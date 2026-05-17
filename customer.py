"""
customer.py — Customer CRM (Mobile-Responsive)
──────────────────────────────────────────────
MOBILE CHANGES:
  - 2-column form collapses gracefully on small screens.
  - Table is wrapped in a horizontal-scroll div.
  - All buttons are touch-friendly (min 44px, CSS-controlled).

PRESERVED BUG FIXES FROM V3:
  - Duplicate phone check via supabase_exists() (non-cached).
  - clear_db_cache() after add to show fresh data immediately.
  - Phone number validation before DB call.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from database import (
    supabase_insert, supabase_select,
    supabase_delete, supabase_exists, clear_db_cache,
)


def customer_module() -> None:
    st.markdown(
        "<h1 style='color:#0f172a;'>🧾 Customer CRM</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#64748b;'>Manage customer profiles and visit history.</p>",
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["➕ Add New", "📋 Directory", "🔍 Search", "🗑️ Delete"])

    # ══════════ ADD ══════════
    with tabs[0]:
        st.subheader("New Customer Profile")
        with st.container(border=True):
            with st.form("add_customer_form", clear_on_submit=True):
                col1, col2 = st.columns([1, 1])
                with col1:
                    name  = st.text_input("Customer Name *", placeholder="e.g. Anjali Kapoor")
                    phone = st.text_input("Phone Number *", placeholder="10-digit mobile")
                with col2:
                    service = st.selectbox("Preferred Service", [
                        "Haircut", "Makeup", "Facial", "Manicure",
                        "Pedicure", "Hair Coloring", "Spa",
                    ])
                    date = st.date_input("Initial Visit Date",
                                        max_value=datetime.now())

                submit = st.form_submit_button(
                    "💾 Save Profile", type="primary", use_container_width=True
                )
                if submit:
                    name_c  = name.strip()
                    phone_c = phone.strip()
                    if not name_c or not phone_c:
                        st.error("❌ Name and Phone are required.")
                    elif not phone_c.isdigit() or len(phone_c) < 7:
                        st.error("❌ Phone must be digits only (min 7 digits).")
                    elif supabase_exists("customers", {"phone": phone_c}):
                        st.warning(f"⚠️ A customer with phone {phone_c} already exists.")
                    else:
                        ok = supabase_insert("customers", {
                            "cust_name":  name_c,
                            "phone":      phone_c,
                            "service":    service,
                            "visit_date": str(date),
                        })
                        if ok:
                            clear_db_cache()
                            st.toast(f"Customer '{name_c}' added!", icon="✅")
                            st.success(f"✅ '{name_c}' added successfully!")

    # ══════════ DIRECTORY ══════════
    with tabs[1]:
        st.subheader("Customer Directory")
        data = supabase_select("customers")
        if data:
            df = pd.DataFrame(data)
            show = [c for c in ["cust_name", "phone", "service", "visit_date"]
                    if c in df.columns]
            df = df[show].copy()
            df.columns = [c.replace("_", " ").title() for c in df.columns]
            st.markdown('<div style="overflow-x:auto;">', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.caption(f"Total: {len(df)} customer(s)")
        else:
            st.info("No customers yet. Start by adding one.")

    # ══════════ SEARCH ══════════
    with tabs[2]:
        st.subheader("Search Customer")
        with st.container(border=True):
            q = st.text_input("Search by Name or Phone", placeholder="Start typing…")
            if st.button("🔍 Search", type="primary", key="cust_search_btn"):
                if q.strip():
                    f = (f"cust_name.ilike.%{q.strip()}%,"
                         f"phone.ilike.%{q.strip()}%")
                    result = supabase_select("customers", or_filter=f)
                    if result:
                        df = pd.DataFrame(result)
                        cols = [c for c in ["cust_name", "phone", "service", "visit_date"]
                                if c in df.columns]
                        st.markdown('<div style="overflow-x:auto;">', unsafe_allow_html=True)
                        st.dataframe(df[cols], use_container_width=True, hide_index=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning(f"No customers matching '{q}'.")
                else:
                    st.warning("Enter a search term.")

    # ══════════ DELETE ══════════
    with tabs[3]:
        st.subheader("Remove Customer")
        with st.container(border=True):
            customers = supabase_select("customers")
            if customers:
                options = {c["phone"]: f"{c.get('cust_name','?')} ({c.get('phone','')})"
                           for c in customers if "phone" in c}
                del_phone = st.selectbox("Select Customer",
                                         list(options.keys()),
                                         format_func=lambda x: options[x])
                st.warning(f"⚠️ This will permanently delete **{options[del_phone]}**.")
                if st.button("🗑️ Confirm Delete", type="primary", key="del_cust_btn"):
                    ok = supabase_delete("customers", {"phone": del_phone})
                    if ok:
                        st.success(f"✅ Customer removed.")
                        st.rerun()
            else:
                st.info("No customers to remove.")
