# 🔐 Onboarding API

Backend for the onboarding flow on [paperwork.framer.ai](https://paperwork.framer.ai/) — handles user registration, authentication, and OTP verification.

---

## How I Built It

### Frontend — Framer
Custom React component with sign in, sign up, OTP verification, and forgot password screens. Google-style minimal dark UI with floating label inputs.

### Backend — Python (FastAPI)
REST API handling user registration and authentication. Users are stored in **Samba Active Directory** via LDAP. OTP codes are delivered via **Gmail SMTP**.

### Infrastructure — Docker + CI/CD
Containerized with Docker, deployed on Oracle Cloud with a free DuckDNS domain and Let's Encrypt SSL. GitHub Actions auto-deploys on every push.

---

## Stack

| What | How |
|---|---|
| Frontend | Framer |
| Domain | [paperwork.framer.ai](https://paperwork.framer.ai/) |
| API | Python (FastAPI) |
| Authentication | Samba Active Directory (LDAP) |
| OTP Delivery | Gmail SMTP |
| Server | Oracle Cloud (Ubuntu) |
| DNS | DuckDNS |
| SSL | Let's Encrypt |
| Container | Docker + Docker Compose |
| CI/CD | GitHub Actions → Docker Hub |

---

## Project Structure

```
onboarding-api/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
├── routes/
│   ├── auth.py          # /signin /register /verify
│   └── forgot.py        # /forgot-password
├── services/
│   ├── otp.py           # OTP generation + storage
│   ├── email_otp.py     # Gmail SMTP delivery
│   └── ad.py            # Samba AD user management
├── models/
│   └── user.py          # Pydantic request models
└── .env.example         # Environment variable template
```

---

## API Endpoints

| Method | Endpoint | What it does |
|---|---|---|
| `POST` | `/register` | Register user, send OTP to email |
| `POST` | `/signin` | Verify credentials, send OTP to email |
| `POST` | `/verify` | Verify OTP code |
| `POST` | `/forgot-password` | Send reset OTP to email |
| `GET` | `/health` | Health check |

---

## Run Locally

```bash
cp .env.example .env
# Fill in your values in .env
docker compose up -d --build
```
