# 💇 Salon Management System V2 (Advance)

![Salon Management ERP System](banner.png)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://salon-management-system-fnmykcwms3nt2mwga9lvbk.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-336791.svg)](https://www.postgresql.org/)
[![Supabase](https://img.shields.io/badge/backend-Supabase-3ECF8E.svg)](https://supabase.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional, industry-standard **Salon Management System** built with Python and Streamlit. This ERP-level application streamlines salon operations, from employee attendance and customer records to appointment scheduling and automated PDF billing.

---

## 🚀 Live Demo
Experience the application live: [Salon Management System Demo](https://salon-management-system-fnmykcwms3nt2mwga9lvbk.streamlit.app/)

> **Credentials:**
> - **Username:** `admin`
> - **Password:** `admin123`

---

## 🌟 Key Features

### 📊 Advanced Dashboard
- **Real-time Analytics**: Track total employees, customers, appointments, and revenue.
- **Visual Insights**: Interactive bar charts showing service popularity.
- **Smart Metrics**: Instant view of the most popular services and financial health.

### 👩‍💼 Employee Management
- **Full CRUD Operations**: Add, view, search, update, and delete staff members.
- **Role Tracking**: Manage stylists, makeup artists, therapists, and receptionists.
- **Salary Management**: Keep track of staff compensation.

### 🧾 Smart Billing & Invoicing
- **Automated PDF Generation**: Generate professional invoices instantly.
- **Downloadable Reports**: Export billing history to CSV for bookkeeping.
- **Service Selection**: Pre-defined service categories with custom pricing.

### 📅 Appointment & Attendance
- **Scheduling**: Book appointments for customers with specific services and stylists.
- **Attendance Tracker**: Mark and monitor staff daily attendance (Present/Absent/Half-day).
- **History Tracking**: View comprehensive visit and attendance history.

### 🔍 Global Search
- **Unified Search**: Quickly find records across the entire database using a centralized search module.

---

## 📸 Screenshots

| Login Interface | Main Dashboard |
| :---: | :---: |
| ![Login Screen](screenshots/login.png) | ![Dashboard](screenshots/dashboard.png) |

| Employee Management | Appointment Scheduler |
| :---: | :---: |
| ![Employee Management](screenshots/Employee%20Management.png) | ![Appointments](screenshots/Appointments.png) |

---

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (for a modern, interactive UI)
- **Backend**: Python 3
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL) - Persistent and production-ready
- **PDF Generation**: [ReportLab](https://www.reportlab.com/)
- **Data Manipulation**: Pandas
- **Styling**: Custom CSS for premium aesthetics

---

## 🚀 The Upgrade: Why Supabase (PostgreSQL)?

Previously, this project used **SQLite3**. While great for local development, it had significant limitations for a modern web application:

1. **Persistence on Streamlit Cloud**: SQLite creates a local file. On hosting platforms like Streamlit Cloud, these files are **deleted** every time the app reboots or you push a code update. Supabase keeps your data safe and permanent.
2. **Production-Ready Scaling**: PostgreSQL is a world-class database built to handle thousands of concurrent users and complex queries that SQLite struggles with.
3. **Cloud Accessibility**: By using a hosted DB, your data is accessible from anywhere, allowing for multi-device synchronization and professional-grade security.

---

## 📁 Project Structure

```text
Salon-Management-System/
├── app.py              # Main entry point & routing
├── database.py         # DB schema & connection logic
├── auth.py             # User authentication system
├── employee.py         # Employee management module
├── customer.py         # Customer records module
├── appointment.py      # Scheduling system
├── attendance.py       # Staff attendance tracker
├── billing.py          # Invoice generation & billing
├── invoice.py          # PDF generation engine
├── search.py           # Global search functionality
├── style.py            # Custom CSS styling
├── requirements.txt    # Project dependencies
└── banner.png          # README header image
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8 or higher installed on your system.

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/ItsMeTinku/Salon-Management-System.git
   cd Salon-Management-System
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

---

## 📖 Usage Instructions

1. **Login**: Use the default credentials (`admin` / `admin123`) to access the dashboard.
2. **Setup Staff**: Navigate to the **Employees** tab to add your salon staff.
3. **Manage Customers**: Record customer details in the **Customers** section.
4. **Book Appointments**: Use the **Appointments** tab to schedule visits.
5. **Generate Bills**: After a service, go to **Billing** to generate and download a PDF invoice.
6. **Track Attendance**: Mark staff attendance daily for payroll accuracy.

---

## 🌐 Deployment

This project is optimized for deployment on **Streamlit Cloud**:
1. Connect your GitHub repository to Streamlit Cloud.
2. Go to **Settings > Secrets** in Streamlit Cloud.
3. Add your Supabase credentials (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`).
4. The system will automatically initialize the PostgreSQL tables on first run.

---

## 🔮 Future Improvements

- [ ] **SMS Integration**: Send appointment reminders via Twilio or similar APIs.
- [ ] **Role-Based Access**: Multi-level access for Staff vs. Managers.
- [x] **Cloud Database**: Migration to PostgreSQL (Supabase) for persistence.
- [ ] **Inventory Management**: Track salon products and low-stock alerts.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the system:
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git checkout origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📧 Contact

**Project Creator** - [ItsMeTinku](https://github.com/ItsMeTinku)  
**Live Demo**: [https://salon-management-system-fnmykcwms3nt2mwga9lvbk.streamlit.app/](https://salon-management-system-fnmykcwms3nt2mwga9lvbk.streamlit.app/)

---
*Created with ❤️ for the Salon Industry.*
