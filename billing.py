import streamlit as st
import pandas as pd
from datetime import datetime
from database import c, conn
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

        service = st.selectbox("Service", [
            "Haircut", "Makeup", "Facial", "Manicure", "Pedicure"
        ])

        amount = st.number_input("Amount", min_value=0)

        if st.button("Generate Bill"):

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            c.execute(
                "INSERT INTO billing VALUES (?,?,?,?)",
                (name, service, str(amount), date)
            )
            conn.commit()

            #  PDF GENERATION
            pdf_file = generate_invoice(name, service, amount)

            st.success("Invoice Generated")

            with open(pdf_file, "rb") as f:
                st.download_button(
                    "📄 Download Invoice PDF",
                    f,
                    file_name=pdf_file
                )

    # ================= VIEW =================
    elif action == "View":

        st.subheader("📋 All Bills")

        data = c.execute("SELECT * FROM billing").fetchall()

        if data:
            df = pd.DataFrame(data, columns=["Customer","Service","Amount","Date"])
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')

            st.download_button(
                "⬇ Export CSV",
                csv,
                "billing_report.csv",
                "text/csv"
            )
        else:
            st.info("No data")