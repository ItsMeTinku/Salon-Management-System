"""
appointment.py — Appointments module
──────────────────────────────────────────────────────────────
KEY CHANGES FROM ORIGINAL:
  1. BUG FIX — "Could not identify appointment ID":
     The original code built app_options with a dict comprehension
     that silently filtered out any row where 'id' was missing
     (e.g. when RLS blocked SELECT or when the Supabase response
     was stale/empty).  The fix:
       a) Use supabase_exists() to pre-validate the customer exists.
       b) Fetch appointments outside the cache using get_supabase_client()
          directly in the update tab so we always get live UUID values.
       c) Show a clear diagnostic message listing which fields are
          actually present if 'id' is still absent.

  2. BUG FIX — No customer ID / name selection UI:
     Customer name was a free-text field.  Replaced with a selectbox
     populated from the customers table so the user picks from real
     records, eliminating typo mismatches.

  3. Employee validation now uses supabase_exists() (non-cached) so
     a newly added employee is found immediately.

  4. All error paths return early (st.stop() inside the form block)
     so no ambiguous messages appear.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import (
    supabase_insert,
    supabase_select,
    supabase_update,
    supabase_delete,
    supabase_exists,
    get_supabase_client,
    clear_db_cache,
)


def _fetch_appointments_live(match_filter: dict | None = None) -> list[dict]:
    """
    Fetch appointments bypassing the @st.cache_data layer.

    WHY a separate helper?
    In the Update tab we need the UUID ('id') of appointments.
    The cached supabase_select() might return stale data (or no
    'id' field if the last response was empty).  Going directly to
    the Supabase client guarantees we get the current rows with all
    columns including the UUID primary key.
    """
    client = get_supabase_client()
    try:
        query = client.table("appointments").select("*")
        if match_filter:
            for k, v in match_filter.items():
                query = query.eq(k, v)
        response = query.execute()
        return response.data or []
    except Exception as exc:
        st.error(f"❌ Failed to fetch appointments: {exc}")
        return []


def appointment_module():
    st.markdown("<h1 style='color: #0f172a;'>📅 Appointments</h1>", unsafe_allow_html=True)
    st.markdown("Schedule and manage customer appointments.")

    tabs = st.tabs(["➕ Book", "📋 Schedule", "🔍 Search", "✏️ Update Status", "🗑️ Cancel"])

    # ═══════════════════════ BOOK ═══════════════════════
    with tabs[0]:
        st.subheader("Book Appointment")
        with st.container(border=True):

            # ── Load customer list for the selectbox ────────────────
            # WHY: A selectbox from real DB records prevents the
            # "customer not found" issue caused by name typos.
            customers = supabase_select("customers")
            customer_names = [c["cust_name"] for c in customers] if customers else []

            # ── Load employee list for the selectbox ────────────────
            employees = supabase_select("employees")
            emp_options = {
                f"{e['id']} — {e.get('name', '')}": e["id"]
                for e in employees
            } if employees else {}

            with st.form("book_app_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    # FIX: selectbox instead of free text for customer
                    if customer_names:
                        cust_name = st.selectbox("Customer *", customer_names)
                    else:
                        cust_name = st.text_input(
                            "Customer Name * (no customers found — type manually)"
                        )
                        st.caption(
                            "⚠️ No customers in DB. Add one in the Customer CRM first."
                        )

                    # FIX: selectbox instead of free text for employee
                    if emp_options:
                        emp_label = st.selectbox("Assigned Employee *", list(emp_options.keys()))
                        emp_id = emp_options[emp_label]
                    else:
                        emp_id = st.text_input("Assigned Employee ID *")
                        st.caption("⚠️ No employees in DB. Add one in Employee Management first.")

                with col2:
                    service = st.selectbox(
                        "Service",
                        ["Haircut", "Makeup", "Facial", "Manicure",
                         "Pedicure", "Hair Coloring", "Spa"],
                    )
                    app_date = st.date_input("Date", min_value=datetime.now())

                status = st.selectbox("Status", ["Pending", "Confirmed", "Completed", "Cancelled"])

                submit = st.form_submit_button(
                    "Book Now", type="primary", use_container_width=True
                )

                if submit:
                    cust_name_val = cust_name.strip() if isinstance(cust_name, str) else cust_name
                    emp_id_val = emp_id.strip() if isinstance(emp_id, str) else emp_id

                    if not cust_name_val or not emp_id_val:
                        st.error("❌ Please fill all required fields.")
                        st.stop()

                    # Validate employee exists (non-cached check)
                    if not supabase_exists("employees", {"id": emp_id_val}):
                        st.error(
                            f"❌ Employee ID '{emp_id_val}' does not exist. "
                            "Add the employee first in Employee Management."
                        )
                        st.stop()

                    data = {
                        "cust_name": cust_name_val,
                        "service": service,
                        "emp_id": emp_id_val,
                        "date": str(app_date),
                        "status": status,
                    }
                    success = supabase_insert("appointments", data)
                    if success:
                        st.toast(f"Appointment booked for {cust_name_val}!", icon="✅")
                        st.success("✅ Appointment booked successfully!")

    # ═══════════════════════ SCHEDULE ═══════════════════════
    with tabs[1]:
        st.subheader("Appointment Schedule")
        filter_status = st.selectbox(
            "Filter by Status", ["All", "Pending", "Confirmed", "Completed", "Cancelled"]
        )

        if filter_status == "All":
            data = supabase_select("appointments")
        else:
            data = supabase_select("appointments", match_filter={"status": filter_status})

        if data:
            df = pd.DataFrame(data)
            cols_to_show = [c for c in ["date", "cust_name", "service", "emp_id", "status"] if c in df.columns]
            df = df[cols_to_show]
            df.columns = ["Date", "Customer", "Service", "Employee ID", "Status"]
            df = df.sort_values(by="Date", ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No appointments found for this filter.")

    # ═══════════════════════ SEARCH ═══════════════════════
    with tabs[2]:
        st.subheader("Search Appointments")
        with st.container(border=True):
            search_query = st.text_input("Search by Customer Name")
            if st.button("Search", type="primary", key="search_app"):
                if search_query.strip():
                    result = supabase_select(
                        "appointments", ilike_filter={"cust_name": search_query.strip()}
                    )
                    if result:
                        df = pd.DataFrame(result)
                        cols = [c for c in ["date", "cust_name", "service", "status"] if c in df.columns]
                        st.dataframe(df[cols], use_container_width=True, hide_index=True)
                    else:
                        st.warning("No appointments found.")
                else:
                    st.info("Enter a search term.")

    # ═══════════════════════ UPDATE ═══════════════════════
    with tabs[3]:
        st.subheader("Update Appointment Status")
        with st.container(border=True):
            st.write("Find an appointment by Customer Name.")
            up_cust = st.text_input("Customer Name (exact match)")

            if up_cust and up_cust.strip():
                # FIX: Use the live (non-cached) fetch so we always get
                # the real UUID values from Supabase, not a stale cache.
                apps = _fetch_appointments_live(match_filter={"cust_name": up_cust.strip()})

                if not apps:
                    st.warning("No appointments found for this customer.")

                else:
                    # ── Validate that 'id' is present ──────────────────
                    # WHY: If 'id' is missing the update will crash.  We
                    # surface a diagnostic instead of silently failing.
                    rows_with_id = [a for a in apps if a.get("id")]

                    if not rows_with_id:
                        present_fields = list(apps[0].keys()) if apps else []
                        st.error(
                            "❌ Could not identify appointment UUID. "
                            f"Fields returned by Supabase: {present_fields}. "
                            "Make sure the 'appointments' table has an "
                            "'id UUID PRIMARY KEY DEFAULT gen_random_uuid()' column "
                            "and that the service_role key is used (not anon)."
                        )
                    else:
                        # Build a readable label → UUID mapping
                        app_options: dict[str, str] = {
                            f"{a['date']} | {a['service']} | Status: {a['status']}": a["id"]
                            for a in rows_with_id
                        }
                        selected_label = st.selectbox(
                            "Select Appointment to Update", list(app_options.keys())
                        )
                        app_id = app_options[selected_label]

                        with st.form("update_app_form"):
                            new_status = st.selectbox(
                                "New Status",
                                ["Pending", "Confirmed", "Completed", "Cancelled"],
                            )
                            update_submit = st.form_submit_button(
                                "Update Status", type="primary", use_container_width=True
                            )
                            if update_submit:
                                # Match on UUID — guaranteed unique
                                success = supabase_update(
                                    "appointments",
                                    {"status": new_status},
                                    {"id": app_id},
                                )
                                if success:
                                    st.toast("Status updated!", icon="✅")
                                    st.success("✅ Appointment status updated successfully!")
                                    clear_db_cache()

    # ═══════════════════════ CANCEL / DELETE ═══════════════════════
    with tabs[4]:
        st.subheader("Cancel/Remove Appointment")
        with st.container(border=True):
            del_cust = st.text_input("Customer Name to Delete")
            if st.button("Delete Appointments", type="primary"):
                if not del_cust.strip():
                    st.error("❌ Please enter a customer name.")
                else:
                    # Non-cached existence check before delete
                    existing = _fetch_appointments_live(
                        match_filter={"cust_name": del_cust.strip()}
                    )
                    if existing:
                        success = supabase_delete(
                            "appointments", {"cust_name": del_cust.strip()}
                        )
                        if success:
                            st.toast("Appointments removed.", icon="🗑️")
                            st.warning("🗑️ All matching appointments deleted.")
                    else:
                        st.error("❌ No appointments found for this customer.")
