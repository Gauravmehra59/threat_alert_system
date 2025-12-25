# Threat Monitoring & Alert Management Platform

A scalable, security-first **Backend REST API** designed to ingest security events and automatically generate alerts for high-severity threats.
Built for the **Cyethack Solutions – Developer Assignment**.

---

## 📌 Project Overview

The Threat Alert System acts as a centralized backend for real-time threat monitoring.
It ingests logs from multiple sources (Firewalls, CCTV, Servers, etc.) via REST APIs.
When a **HIGH** or **CRITICAL** severity event is detected, the system **automatically creates an alert** for analysts to review.

---

## ✨ Key Features

* **🚀 Event Ingestion**

  * High-performance API to receive security logs in real time.

* **⚡ Automated Alerting**

  * Uses **Django Signals** to auto-generate alerts for `HIGH` and `CRITICAL` events.

* **🔐 Role-Based Access Control (RBAC)**

  * **Analyst:** Read-only access to view and filter alerts.
  * **Admin:** Full access to manage alerts and update status (OPEN → RESOLVED).

* **🛡️ Security Best Practices**

  * **JWT Authentication** (SimpleJWT)
  * **API Throttling** to prevent brute-force / DDoS attacks
  * **Audit Logging** for critical actions (alert creation & updates)

---

## 🛠️ Tech Stack

* **Backend:** Python 3.10+, Django 5.x
* **API Framework:** Django REST Framework (DRF)
* **Authentication:** SimpleJWT (JWT-based Auth)
* **Database:** SQLite (default) / PostgreSQL (supported)
* **Testing:** Django `APITestCase`

---

## 🏗️ System Architecture

```mermaid
graph TD
    User[Analyst / Admin] -->|HTTP Request + JWT| API[Django REST API]
    Sensor[Firewall / Camera] -->|POST Event| API

    subgraph Backend Core
        API --> Auth[JWT Auth & Throttling]
        Auth --> View[Views & Business Logic]
        View --> Serializer[Serializers]
        Serializer --> DB[(Database)]

        DB -->|Event Saved| Signal[post_save Signal]
        Signal --> Decision{Severity HIGH / CRITICAL?}
        Decision -->|Yes| Alert[Create Alert]
        Alert --> DB
    end
```

---

## ⚙️ Setup Instructions

Follow the steps below to run the project locally.

---

### 1️⃣ Clone the Repository

```bash
git clone <PASTE_YOUR_GITHUB_REPO_LINK_HERE>
cd threat_alert_system
```

---

### 4️⃣ Environment Configuration (`.env`)

Create a `.env` file in the root directory:

```ini
DEBUG=True
SECRET_KEY=your_secret_random_key
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

### 5️⃣ Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6️⃣ Create Admin User

```bash
python manage.py createsuperuser
```

---

### 7️⃣ Run Development Server

```bash
python manage.py runserver
```

Access the API at:
👉 **[http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)**

---

## 📡 API Endpoints

### 🔐 Authentication

| Method | Endpoint         | Description                  |
| ------ | ---------------- | ---------------------------- |
| POST   | `/auth/login/`   | Obtain Access & Refresh JWT  |
| POST   | `/auth/refresh/` | Refresh expired Access Token |

---

### 📥 Events (Ingestion)

| Method | Endpoint          | Description              | Access              |
| ------ | ----------------- | ------------------------ | ------------------- |
| POST   | `/event/ingest/` | Log a new security event | Authenticated Users |

---

### 🚨 Alerts (Management)

| Method | Endpoint                 | Description                 | Access        |
| ------ | ------------------------ | --------------------------- | ------------- |
| GET    | `/alerts/`               | List all alerts (paginated) | Authenticated |
| GET    | `/alerts/?severity=HIGH` | Filter by severity          | Authenticated |
| GET    | `/alerts/?status=OPEN`   | Filter by status            | Authenticated |
| PATCH  | `/alerts/<id>/`          | Update alert status         | Admin Only    |

---

## ✅ Testing

Automated tests verify core functionality, permissions, and signals.

```bash
python manage.py test
```

### Test Coverage

* **Logic:** HIGH / CRITICAL events auto-create alerts
* **Permissions:** Analysts receive `403 Forbidden` on update attempts
* **API:** Successful event ingestion via REST API

---

## 📝 Assumptions Made

* **Event–Alert Relationship:**
  One-to-One relationship (one high-severity event → one alert)

* **Timezone:**
  All timestamps are stored and returned in **UTC**

* **Source Authentication:**
  Sensors use JWT authentication (API Keys recommended for production)

* **Data Retention:**
  No deletion policy; all events and alerts are retained for audit purposes

---

## 📂 Project Structure

```text
threat_alert_system/
├── core/
│   ├── models.py        # Event & Alert models
│   ├── views.py         # API views & permissions
│   ├── serializers.py  # Validation & serialization
│   ├── signals.py      # Auto-alert logic
│   ├── tests.py        # Unit & integration tests
│   └── urls.py         # App routing
├── logs/                # Audit & security logs
├── manage.py
├── requirements.txt
└── README.md
```

---

## 👨‍💻 Author

**Developed for Cyethack Solutions – Backend Developer Assignment**

Gaurav Mehra
---
