import streamlit as st
import pandas as pd
from datetime import datetime
from database import c, conn

# ================= CUSTOMER MODULE =================
def customer_module():

    st.title("🧾 Customer Management System")

    # ---------- SUBPAGE CONTROL ----------
    if "subpage" not in st.session_state or st.session_state.subpage is None:
        st.session_state.subpage = "Add"

    # ---------- ACTION TABS ----------
    action = st.radio(
        "Select Action",
        ["Add", "View", "Search", "Delete"],
        index=["Add", "View", "Search", "Delete"].index(st.session_state.subpage)
    )

    st.session_state.subpage = action

    # ================= ADD CUSTOMER =================
    if action == "Add":

        st.subheader("➕ Add New Customer")

        name = st.text_input("Customer Name")
        phone = st.text_input("Phone Number")

        service = st.selectbox("Service", [
            "Haircut",
            "Makeup",
            "Facial",
            "Manicure",
            "Pedicure"
        ])

        if st.button("Save Customer", use_container_width=True):

            if name == "" or phone == "":
                st.error("Please fill all fields")
            else:
                c.execute(
                    "INSERT INTO customers VALUES (?,?,?,?)",
                    (name, phone, service, str(datetime.now().date()))
                )
                conn.commit()
                st.success("Customer Added Successfully")

    # ================= VIEW CUSTOMERS =================
    elif action == "View":

        st.subheader("📋 All Customers")

        data = c.execute("SELECT * FROM customers").fetchall()

        if data:
            df = pd.DataFrame(data, columns=["Name", "Phone", "Service", "Date"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No customers found")

    # ================= SEARCH CUSTOMER =================
    elif action == "Search":

        st.subheader("🔍 Search Customer")

        phone = st.text_input("Enter Phone Number")

        if st.button("Search", use_container_width=True):

            result = c.execute(
                "SELECT * FROM customers WHERE phone=?",
                (phone,)
            ).fetchall()

            if result:
                st.table(result)
            else:
                st.warning("No customer found")

    # ================= DELETE CUSTOMER =================
    elif action == "Delete":

        st.subheader("🗑️ Delete Customer")

        phone = st.text_input("Enter Phone Number to Delete")

        if st.button("Delete Customer", use_container_width=True):

            c.execute(
                "DELETE FROM customers WHERE phone=?",
                (phone,)
            )
            conn.commit()

            st.success("Customer Deleted Successfully")