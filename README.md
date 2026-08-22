# Secure Flask Authentication System

> A defensive Flask application demonstrating secure authentication, session management, CSRF protection, password hashing, rate limiting, protected routes, security headers, and automated security testing.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Security](https://img.shields.io/badge/Security-Secure%20Coding-B91C1C?style=for-the-badge)](https://owasp.org/)

## Overview

This project implements a small authentication-focused Flask application designed to demonstrate practical secure-coding controls for web applications.

The application covers the core authentication lifecycle—registration, login, session handling, logout, and protected resources—while adding defensive controls against common web-application threats.

## Security Controls

- Password hashing instead of plaintext password storage
- Session-based authentication
- CSRF protection on state-changing forms
- Login/authentication rate limiting
- Protected application routes
- HTTP security response headers
- Input validation
- Logout/session invalidation
- Automated security-focused tests

## Architecture

```text
              Browser
                 │
                 ▼
          Flask Application
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
 Authentication  CSRF    Security
    Layer       Guard     Headers
       │
       ▼
 Session Management
       │
       ▼
 Password Hashing
       │
       ▼
     SQLite
```

## Authentication Flow

```text
Registration
     ↓
Validate Input
     ↓
Hash Password
     ↓
Persist User

Login
     ↓
Validate Credentials
     ↓
Apply Rate Limit
     ↓
Create Session
     ↓
Protected Dashboard
     ↓
Logout / Invalidate Session
```

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Web framework | Flask |
| Authentication | Session-based authentication |
| Password security | Werkzeug password hashing |
| CSRF | Flask-WTF / CSRF protection |
| Database | SQLite |
| Frontend | HTML / CSS |
| Testing | Python test suite |
| Security reference | OWASP secure-coding principles |

## Project Structure

```text
flask-auth-security/
├── app.py
├── templates/
├── static/
├── tests/
├── requirements.txt
└── README.md
```

> The exact module layout may evolve with the implementation; inspect the repository source for the current structure.

## Getting Started

### Prerequisites

- Python 3.x
- pip
- A local development environment

### Installation

```bash
git clone https://github.com/hack2ai/flask-auth-security.git
cd flask-auth-security
python -m venv venv
```

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

Configure application secrets through environment variables rather than committing them to the repository.

### Run

```bash
python app.py
```

Open the local Flask development server in your browser and test registration, login, the protected dashboard, and logout.

## Testing

Run the project's test suite according to the test configuration in the repository. A useful security-focused test plan should verify:

- Registration validation
- Password hashing
- Successful login
- Invalid credential handling
- Protected-route access control
- CSRF enforcement
- Rate-limit behavior
- Logout/session invalidation
- Security response headers

## Security Engineering Notes

This repository is an educational secure-coding project, **not a security-audited production authentication service**.

A production deployment should additionally consider:

- HTTPS everywhere
- Secure, HttpOnly, and appropriately scoped cookies
- Strong session-secret management and rotation
- Production-grade database configuration
- Account recovery and email verification controls
- Multi-factor authentication where appropriate
- Centralized audit logging
- Dependency vulnerability scanning
- Monitoring and alerting
- Stronger authorization policies for application-specific resources
- Threat modeling and penetration testing

## Responsible Disclosure

If you discover a security issue in this project, avoid publicly exposing sensitive exploit details before the issue can be reviewed. Use the repository's issue/disclosure process where applicable.

## Project Value

This project demonstrates practical **Flask security engineering, authentication design, secure password handling, CSRF defense, session management, rate limiting, HTTP hardening, and automated security testing**.

## Author

**Pankaj (Tony) Kumar**  
AI Engineer • Full Stack Developer • Generative AI & RAG Specialist

[GitHub](https://github.com/hack2ai) • [LinkedIn](https://www.linkedin.com/in/pankaj-kumar-ab591a216)

## License

See the repository license file for the applicable project license.
