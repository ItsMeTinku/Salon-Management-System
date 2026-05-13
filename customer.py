import streamlit as st
import pandas as pd
from datetime import datetime
from database import c, conn, PH

# ═══════════════════════════════════════════════
# CUSTOMER MODULE
# ═══════════════════════════════════════════════
def customer_module():

    st.title("🧾 Customer Management System")

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

        st.subheader("➕ Add New Customer")

        name  = st.text_input("Customer Name")
        phone = st.text_input("Phone Number")
        service = st.selectbox("Service", [
            "Haircut", "Makeup", "Facial", "Manicure", "Pedicure"
        ])

        if st.button("Save Customer", use_container_width=True):
            if not name.strip() or not phone.strip():
                st.error("Please fill all fields.")
            else:
                try:
                    c.execute(
                        f"INSERT INTO customers VALUES ({PH},{PH},{PH},{PH})",
                        (name.strip(), phone.strip(), service, str(datetime.now().date()))
                    )
                    conn.commit()
                    st.success(f"✅ Customer '{name}' added successfully!")
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Error saving customer: {e}")

    # ═══════════════════ VIEW ══════════════════
    elif action == "View":

        st.subheader("📋 All Customers")
        try:
            data = c.execute("SELECT * FROM customers").fetchall()
            if data:
                df = pd.DataFrame(data, columns=["Name", "Phone", "Service", "Date"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No customers found. Add customers first.")
        except Exception as e:
            st.error(f"❌ Error loading customers: {e}")

    # ═══════════════════ SEARCH ════════════════
    elif action == "Search":

        st.subheader("🔍 Search Customer")
        phone = st.text_input("Enter Phone Number")

        if st.button("Search", use_container_width=True):
            try:
                result = c.execute(
                    f"SELECT * FROM customers WHERE phone={PH}",
                    (phone.strip(),)
                ).fetchall()
                if result:
                    df = pd.DataFrame(result, columns=["Name", "Phone", "Service", "Date"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No customer found with that phone number.")
            except Exception as e:
                st.error(f"❌ Search error: {e}")

    # ═══════════════════ DELETE ════════════════
    elif action == "Delete":

        st.subheader("🗑️ Delete Customer")
        phone = st.text_input("Enter Phone Number to Delete")

        if st.button("Delete Customer", use_container_width=True):
            if not phone.strip():
                st.error("Please enter a phone number.")
            else:
                try:
                    c.execute(
                        f"DELETE FROM customers WHERE phone={PH}",
                        (phone.strip(),)
                    )
                    conn.commit()
                    if c.rowcount == 0:
                        st.warning("No customer found with that phone number.")
                    else:
                        st.warning("🗑️ Customer deleted successfully.")
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Delete error: {e}")