# 💇 Salon Management System V3 (Enterprise Upgrade)

![Salon Management ERP System](banner.png)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://salon-management-system-fnmykcwms3nt2mwga9lvbk.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-336791.svg)](https://www.postgresql.org/)
[![Supabase](https://img.shields.io/badge/backend-Supabase-3ECF8E.svg)](https://supabase.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern **Salon Management ERP System** built with **Python**, **Streamlit**, and **Supabase PostgreSQL**.  
This project evolved from a basic CRUD application into a cloud-based management system featuring secure database architecture, UUID-based workflows, advanced validation, PDF billing, attendance tracking, and appointment management.

---

# 🚀 Live Demo

### 🌐 Try the Application
👉 https://salon-management-system-fnmykcwms3nt2mwga9lvbk.streamlit.app/

### 🔑 Demo Credentials
| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |

---

# 🌟 Key Features

## 📊 Advanced Dashboard
- Real-time salon analytics
- Customer, employee, and appointment statistics
- Revenue overview
- Interactive service insights
- Centralized management interface

---

## 👩‍💼 Employee Management
- Add, update, search, and delete employees
- Manage staff roles and salaries
- Employee attendance integration
- Validation-based employee workflows

---

## 👥 Customer Management
- Maintain customer records
- Fast customer lookup
- Integrated appointment linking
- Persistent cloud database storage

---

## 📅 Appointment Management
- Schedule customer appointments
- Assign services and employees
- Update appointment statuses
- UUID-based appointment tracking
- Improved reliability for update/delete operations

---

## 🧾 Smart Billing & Invoicing
- Generate professional PDF invoices
- Download billing reports
- Dynamic service pricing
- Persistent billing history

---

## 🕒 Attendance Tracking
- Daily attendance management
- Present/Absent/Half-day tracking
- Employee existence validation
- Improved data consistency

---

## 🔍 Global Search System
- Unified search across modules
- Faster data access
- Simplified navigation workflow

---

# 🚀 Evolution of the Project (V1 → V2 → V3)

| Version | Architecture | Database | Key Features | Limitations |
|---|---|---|---|---|
| **V1** | Basic CRUD Application | SQLite3 | Employee records, customer management, simple billing | Local-only storage |
| **V2** | Advanced Management System | SQLite3 | Dashboard analytics, PDF invoices, attendance tracking | Data reset issues on cloud deployment |
| **V3 (Current)** | Cloud ERP Architecture | Supabase PostgreSQL | RLS security, UUID workflows, cloud persistence, advanced validation | UI modernization in progress |

---

# 🆕 Major Upgrades in V3

## ☁️ Migration to Supabase PostgreSQL
- Replaced SQLite with Supabase PostgreSQL
- Added persistent cloud-based storage
- Eliminated data loss after redeployment
- Improved scalability and production readiness

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

## 🧠 Advanced Validation System
- Added employee existence validation
- Prevented invalid attendance insertion
- Improved error handling and workflow stability

---

## 📄 Improved PDF Billing Workflow
- Refactored invoice generation logic
- Fixed Streamlit form/download conflicts
- Improved PDF download reliability

---

## ⚡ Live Database Synchronization
- Added live appointment fetching
- Reduced stale cached data issues
- Improved consistency between frontend and database state

---

# 🛠️ Technical Challenges Solved

## 🔐 Supabase Authorization Issues
- Fixed `42501` RLS permission errors
- Configured policies for multiple tables
- Solved authentication-related query failures

---

## 🧩 Database Schema Migration
- Added UUID columns to legacy tables
- Migrated old appointment records safely
- Improved relational consistency

---

## 🔄 Stateful Update Workflows
- Rebuilt update logic using UUID targeting
- Removed unreliable customer-name-based updates

---

## 🧾 Streamlit Form Constraints
- Solved `st.download_button()` form limitations
- Implemented `session_state` persistence

---

## ✅ Validation & Error Handling
- Prevented false success messages
- Added early validation checks
- Improved backend workflow safety

---

# 📸 Screenshots

| Login Interface | Main Dashboard |
| :---: | :---: |
| ![Login Screen](screenshots/login.png) | ![Dashboard](screenshots/dashboard.png) |

| Employee Management | Appointment Scheduler |
| :---: | :---: |
| ![Employee Management](screenshots/Employee%20Management.png) | ![Appointments](screenshots/Appointments.png) |

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

## Architecture Improvements
- PostgreSQL cloud persistence
- UUID-enabled workflows
- Row Level Security (RLS)
- Multi-table relational structure
- Real-time consistency improvements

---

# 📁 Project Structure

```text
Salon-Management-System/
├── app.py              # Main entry point & routing
├── database.py         # Database connection & helpers
├── auth.py             # Authentication logic
├── employee.py         # Employee management module
├── customer.py         # Customer management module
├── appointment.py      # Appointment scheduling system
├── attendance.py       # Attendance tracker
├── billing.py          # Billing & invoice logic
├── invoice.py          # PDF invoice engine
├── search.py           # Global search system
├── style.py            # Custom UI styling
├── requirements.txt    # Dependencies
└── banner.png          # README assets
```

---

# ⚙️ Installation & Setup

## Prerequisites
- Python 3.9+
- Git
- Supabase Account

---

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

### Linux / macOS
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
7. Track salon operations through dashboard analytics

---

# 🌐 Deployment

Optimized for deployment on:

- Streamlit Cloud
- Render
- Railway
- VPS environments

## Deployment Steps
1. Push repository to GitHub
2. Connect repo to Streamlit Cloud
3. Add Supabase secrets
4. Deploy application

---

# 📈 Engineering Progress

This project evolved from:

```text
Basic CRUD Desktop-Style Application
```

into:

```text
Cloud-Based Salon ERP System with Secure Backend Architecture
```

The V3 upgrade focused heavily on:
- backend engineering
- database authorization
- schema design
- debugging production-style workflows
- validation systems
- scalable architecture

rather than only adding frontend features.

---

# 🔮 Future Improvements (V4 Roadmap)

- [ ] Modern dashboard redesign
- [ ] Role-based authentication
- [ ] Advanced analytics & charts
- [ ] Inventory management
- [ ] SMS/WhatsApp reminders
- [ ] Payroll management
- [ ] API abstraction layer
- [ ] Activity logging system
- [ ] Mobile responsive redesign

---

# 🤝 Contributing

Contributions are welcome.

## Steps
1. Fork the repository
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

This project represents the evolution from a beginner CRUD application into a structured cloud-based management system focused on real-world backend workflows, validation systems, and production-style debugging experience.
