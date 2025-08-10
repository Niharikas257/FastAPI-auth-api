# FastAPI Auth API (JWT + PostgreSQL + Docker)

A production-style authentication REST API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, and **JWT**.  
Runs with a single command using **Docker Compose** — complete with a persistent PostgreSQL volume, health checks, and automated migrations.

---

## 🚀 Features
- **User Signup & Login** with hashed passwords (bcrypt)
- **JWT Authentication** for secure protected endpoints
- **PostgreSQL** + **SQLAlchemy ORM**
- **Alembic Migrations** for database schema changes
- **Dockerfile + Docker Compose** for API + DB + persistent storage
- **Automatic DB Migrations** on container startup
- Health check endpoint (`/healthz`) for uptime monitoring
- Ready for observability integration (Prometheus/Grafana)

---

## 🛠️ Tech Stack
- **Language:** Python 3.11
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Auth:** JWT (JSON Web Tokens)
- **Containerization:** Docker, Docker Compose

---

## 📡 API Endpoints
| Method | Endpoint       | Description           | Auth Required |
| ------ | -------------- | --------------------- | ------------- |
| POST   | `/auth/signup` | Create a new account  | ❌             |
| POST   | `/auth/login`  | Login & get JWT token | ❌             |

---

## ⚙️ Setup & Run

### Prerequisites
- Docker & Docker Compose  
- (Optional for local dev) Python 3.11+, pip, virtualenv  
- Git  

---

### 1) Clone the repo
`git clone https://github.com/<your-username>/fastapi-auth-api.git && cd fastapi-auth-api`

---

### 2) Configure environment  
Copy `.env.example` to `.env` and set a unique `SECRET_KEY` (and any DB values you want):  
`cp .env.example .env`

---

### 3) Run with Docker (recommended)  
`docker compose up --build -d`  
API: [http://localhost:8000](http://localhost:8000)  
Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  

View logs:  
`docker compose logs -f api`  

Stop:  
`docker compose down`

---

### 4) Quick test

#### PowerShell (Windows)
`Invoke-WebRequest -Uri "http://localhost:8000/auth/signup" -Method POST -ContentType "application/json" -Body '{"email":"a@b.com","password":"secret"}'`

`$response = Invoke-WebRequest -Uri "http://localhost:8000/auth/login" -Method POST -ContentType "application/json" -Body '{"email":"a@b.com","password":"secret"}'`

`$token = ($response.Content | ConvertFrom-Json).access_token; $token`

#### curl (macOS/Linux or Git Bash)
`curl -X POST "http://localhost:8000/auth/signup" -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"secret"}'`

`curl -X POST "http://localhost:8000/auth/login" -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"secret"}'`

---

### 5) Run locally (no Docker)
`python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)  
`pip install -r requirements.txt`  
`alembic upgrade head`  
`uvicorn app.main:app --reload`  
API: [http://localhost:8000](http://localhost:8000)  
Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 6) Migrations (Alembic)
`alembic revision --autogenerate -m "your message" && alembic upgrade head`

---

### 7) Tests (if present)
`pytest -q`

---

### Common Docker commands
`docker compose ps` → show running services  
`docker compose logs -f api` → tail API logs  
`docker compose restart api` → restart API  
`docker compose down -v` → stop & remove volumes (resets DB)
