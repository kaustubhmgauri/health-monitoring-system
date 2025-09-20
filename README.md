# Heart Rate Monitoring System (HRMS)

A modular **Django REST Framework** backend for monitoring patient heart rate and managing related data.  
The system is designed for scalability and separation of concerns with modular apps: **users**, **patients**, and **vitals**.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Postman Example Payloads](#postman-example-payloads)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

The **Heart Rate Monitoring System (HRMS)** provides:

- Secure user registration and authentication
- Patient management with CRUD operations
- Recording and retrieving patient vitals (heart rate)
- Advanced search, filtering, ordering, and pagination
- Modular architecture for maintainability and scalability

---

## Architecture

- **Modular Django Apps**
  - `users` - Authentication, registration, and admin management
  - `patients` - Patient CRUD operations, search, and filtering
  - `vitals` - Heart rate recording and monitoring

- **RESTful APIs** with **Django REST Framework**
- **JWT Authentication** for secure access
- **PostgreSQL** as the primary database

---

## Features

### Users
- Register and login
- JWT authentication
- Admin-only: list all users
- Role-based access

### Patients
- Create, read, update, delete patients
- Associate patients with a user (doctor/admin)
- Search, filter, and pagination support

### Vitals
- Record heart rate for patients
- Retrieve paginated and searchable heart rate records
- Link records to the user who recorded them

---

## Technology Stack

| Layer            | Technology / Library           |
|-----------------|-------------------------------|
| Backend          | Python, Django, DRF           |
| Authentication   | JWT (djangorestframework-simplejwt) |
| Database         | PostgreSQL                    |
| Testing          | Pytest, pytest-django         |
| Environment      | Python-dotenv (.env)          |
| Deployment       | Docker                        |  |

---

## Setup & Installation

1. **Clone the repository**
```bash
git clone <repo-url>
cd heart-rate-monitoring

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

SECRET_KEY=your-django-secret-key
DEBUG=True
API_VERSION=v1
DATABASE_URL=postgres://user:password@localhost:5432/hrms_db

python manage.py runserver

| Endpoint                    | Method | Description                |
| --------------------------- | ------ | -------------------------- |
| `/api/v1/users/auth/register`   | POST   | Register a new user        |
| `/api/v1/users/auth/login`      | POST   | Login and get JWT tokens   |
| `/api/v1/users/auth/list-users` | GET    | Admin-only: list all users |


| Endpoint                 | Method    | Description                           |
| ------------------------ | --------- | ------------------------------------- |
| `/api/v1/patients`      | GET       | List patients (search/order/paginate) |
| `/api/v1/patients`      | POST      | Create a patient                      |
| `/api/v1/patients/{id}` | PUT/PATCH | Update a patient                      |
| `/api/v1/patients/{id}` | DELETE    | Delete a patient                      |

| Endpoint               | Method | Description                |
| ---------------------- | ------ | -------------------------- |
| `/api/v1/vitals/heart-rates` | GET    | List heart rate records    |
| `/api/v1/vitals/heart-rates` | POST   | Create a heart rate record |


POST /api/v1/users/auth/register
{
  "username": "doctor1",
  "password": "securepassword123"
}

POST /api/v1/users/auth/login
{
  "username": "doctor1",
  "password": "securepassword123"
}

POST /api/v1/patients
Authorization: Bearer <JWT_TOKEN>
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1980-05-15",
  "gender": "Male",
  "email": "john.doe@example.com",
  "contact_number": "1234567890",
  "place": 1  # Location ID
}

POST /api/v1/vitals/heart-rates
Authorization: Bearer <JWT_TOKEN>
{
  "patient": 1,  # Patient ID
  "bpm": 78
}


python manage.py test


heart_rate_monitoring/
│
├─ users/
│  ├─ models.py
│  ├─ serializers.py
│  ├─ views.py
│  └─ urls.py
│
├─ patients/
│  ├─ models.py
│  ├─ serializers.py
│  ├─ views.py
│  └─ urls.py
│
├─ vitals/
│  ├─ models.py
│  ├─ serializers.py
│  ├─ views.py
│  └─ urls.py
│
├─ manage.py
├─ requirements.txt
├─ .env
└─ README.md
