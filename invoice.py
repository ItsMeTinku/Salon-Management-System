from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit as st

def generate_invoice(name, service, amount):

    file_name = f"{name}_invoice.pdf"

    c = canvas.Canvas(file_name, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "Salon Invoice")

    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Customer: {name}")
    c.drawString(100, 720, f"Service: {service}")
    c.drawString(100, 690, f"Amount: ₹{amount}")

    c.drawString(100, 640, "Thank you for visiting our salon!")

    c.save()

    return file_name