from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def generate_invoice(name, service, amount):

    # Use /tmp on Streamlit Cloud (read-only source dir), local dir otherwise
    if os.path.isdir("/tmp") and os.access("/tmp", os.W_OK):
        output_dir = "/tmp"
    else:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    file_name = os.path.join(output_dir, f"{name}_invoice.pdf")

    c = canvas.Canvas(file_name, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "Salon Invoice")

    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Customer: {name}")
    c.drawString(100, 720, f"Service: {service}")
    c.drawString(100, 690, f"Amount: Rs.{amount}")

    c.drawString(100, 640, "Thank you for visiting our salon!")

    c.save()

    return file_name