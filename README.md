# 💇 Salon Management System V3 (Enterprise Upgrade)

![Salon Management ERP System](banner.png)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://salon-management-system-fnmykcwms3nt2mwga9lvbk.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-336791.svg)](https://www.postgresql.org/)
[![Supabase](https://img.shields.io/badge/backend-Supabase-3ECF8E.svg)](https://supabase.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern **Salon Management ERP System** built with **Python**, **Streamlit**, and **Supabase PostgreSQL**.

This project evolved from a basic CRUD application into a cloud-based salon ERP platform featuring:

- Secure backend architecture
- UUID-based appointment workflows
- Row Level Security (RLS)
- Advanced validation systems
- PDF invoice generation
- Attendance & employee management
- Modernized professional UI/UX
- Real-time cloud persistence

---

# 🚀 Live Demo

### 🌐 Application Link
👉 https://salon-management-system-fnmykcwms3nt2mwga9lvbk.streamlit.app/

### 🔑 Demo Credentials

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |

---

# 🌟 Key Features & UI Highlights

## 📊 Advanced Dashboard
- Real-time analytics
- Revenue insights
- Appointment statistics
- Service popularity tracking
- Professional ERP-style interface

---

## 👩‍💼 Employee Management
- Add/update/delete employees
- Salary management
- Role tracking
- Attendance integration
- Validation-based workflows

---

## 👥 Customer Management
- Cloud-based customer records
- Fast customer lookup
- Integrated appointment linking
- Persistent storage using PostgreSQL

---

## 📅 Appointment Management
- Schedule appointments
- Assign employees/services
- UUID-based appointment updates
- Improved reliability and validation

---

## 🧾 Smart Billing System
- PDF invoice generation
- Downloadable billing reports
- Persistent billing history
- Improved billing workflows

---

## 🕒 Attendance Tracking
- Daily attendance management
- Present/Absent/Half-day tracking
- Employee validation system
- Improved workflow consistency

---

## 🔍 Global Search
- Unified search system
- Cross-module record searching
- Faster navigation experience

---

# 🚀 Project Evolution (V1 → V2 → V3)

| Version | Architecture | Database | Highlights |
|---|---|---|---|
| **V1** | Basic CRUD Application | SQLite3 | Core management features |
| **V2** | Advanced Management System | SQLite3 | Analytics, PDF billing, attendance |
| **V3** | Cloud ERP Architecture | Supabase PostgreSQL | RLS security, UUID workflows, cloud persistence, professional UI |

---

# 🎨 UI Evolution (Old vs New)

## 🔐 Login Interface Upgrade

| Previous UI | V3 Redesigned UI |
| :---: | :---: |
| ![Old Login](screenshots/login.png) | ![New Login](screenshots/loginnew.png) |

---

## 📊 Dashboard Upgrade

| Previous Dashboard | V3 Dashboard |
| :---: | :---: |
| ![Old Dashboard](screenshots/dashboard.png) | ![New Dashboard](screenshots/dashboardnew.png) |

---

## 👩‍💼 Employee Management Upgrade

| Previous Employee UI | V3 Employee UI |
| :---: | :---: |
| ![Old Employee UI](screenshots/Employee%20Management.png) | ![New Employee UI](screenshots/Employee%20Managementnew.png) |

---

## 📅 Appointment Module Upgrade

| Previous Appointment UI | V3 Appointment UI |
| :---: | :---: |
| ![Old Appointment UI](screenshots/Appointments.png) | ![New Appointment UI](screenshots/Appointmentsnew.png) |

---

# 🆕 Major Upgrades in V3

## ☁️ Migration to Supabase PostgreSQL
- Replaced SQLite with Supabase PostgreSQL
- Added persistent cloud-based storage
- Eliminated data loss after redeployment
- Improved scalability and reliability

---

## 🔒 Row Level Security (RLS)
- Implemented secure database access policies
- Configured INSERT/SELECT permissions
- Improved backend security architecture

---

## 🆔 UUID-Based Appointment System
- Migrated appointments to UUID-based identification
- Prevented duplicate-name conflicts
- Improved update/delete reliability

---

## 🧠 Advanced Validation & Error Handling
- Added employee existence validation
- Prevented invalid attendance insertions
- Improved workflow reliability

---

## 📄 Improved PDF Billing Workflow
- Fixed Streamlit form/download conflicts
- Refactored invoice download flow
- Improved billing stability

---

## ⚡ Live Database Synchronization
- Added live appointment fetching
- Reduced stale cached data
- Improved frontend/database consistency

---

# 🛠️ Technical Challenges Solved

## 🔐 Supabase Authorization Debugging
- Fixed `42501` RLS permission errors
- Implemented multi-table policies
- Solved authentication query failures

---

## 🧩 Database Schema Migration
- Added UUID columns to appointment records
- Migrated existing records safely
- Improved database consistency

---

## 🔄 Stateful Update Workflows
- Rebuilt appointment update logic using UUID targeting
- Removed unreliable customer-name matching

---

## 🧾 Streamlit Form Constraints
- Solved `st.download_button()` limitations inside forms
- Implemented `session_state` persistence workflow

---

## ✅ Validation Architecture
- Prevented false success messages
- Added early validation checks
- Improved backend workflow safety

---

# 📸 Current V3 Screenshots

| Login Interface | Dashboard |
| :---: | :---: |
| ![Login](screenshots/loginnew.png) | ![Dashboard](screenshots/dashboardnew.png) |

| Employee Management | Appointments |
| :---: | :---: |
| ![Employees](screenshots/Employee%20Managementnew.png) | ![Appointments](screenshots/Appointmentsnew.png) |

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| Database | Supabase PostgreSQL |
| PDF Engine | ReportLab |
| Data Handling | Pandas |
| Styling | Custom CSS |

---

# 🧱 Database Architecture

## Current Tables

```text
admin
appointments
attendance
billing
customers
employees
```

## Core Improvements
- PostgreSQL cloud persistence
- UUID-enabled workflows
- Row Level Security (RLS)
- Multi-table relational structure
- Real-time consistency improvements

---

# 📁 Project Structure

```text
Salon-Management-System/
├── app.py
├── database.py
├── auth.py
├── employee.py
├── customer.py
├── appointment.py
├── attendance.py
├── billing.py
├── invoice.py
├── search.py
├── style.py
├── requirements.txt
├── screenshots/
└── banner.png
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/ItsMeTinku/Salon-Management-System.git
cd Salon-Management-System
```

---

## 2️⃣ Create Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Supabase Secrets

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_anon_key"
```

---

## 5️⃣ Run Application

```bash
streamlit run app.py
```

---

# 📖 Usage Workflow

1. Login using admin credentials
2. Add salon employees
3. Register customers
4. Schedule appointments
5. Mark attendance
6. Generate invoices
7. Monitor salon analytics

---

# 🌐 Deployment

Optimized for:
- Streamlit Cloud
- Render
- Railway
- VPS hosting

---

# 📈 Engineering Progress

This project evolved from:

```text
Basic CRUD Desktop Application
```

into:

```text
Cloud-Based Salon ERP System with Secure Backend Architecture
```

The V3 upgrade focused heavily on:
- backend engineering
- cloud database integration
- schema design
- debugging workflows
- validation systems
- UI modernization
- scalable architecture

---

# 🔮 Future Improvements (V4 Roadmap)

- [ ] Role-based authentication
- [ ] Inventory management
- [ ] SMS/WhatsApp reminders
- [ ] Payroll management
- [ ] Advanced analytics & charts
- [ ] Mobile responsive redesign
- [ ] Activity logging system
- [ ] API abstraction layer

---

# 🤝 Contributing

Contributions are welcome.

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push branch
5. Open Pull Request


---

# 👨‍💻 Developer

## Tinku
GitHub: https://github.com/ItsMeTinku

---

# ❤️ Final Note

This project represents the transition from a beginner CRUD application into a structured cloud-based ERP management system focused on real-world backend workflows, secure database architecture, validation systems, and professional UI/UX design.
