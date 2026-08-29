# Secure Flask Authentication System

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![Security](https://img.shields.io/badge/Security-Secure%20Coding-B91C1C?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-5%20passed-2EA44F?style=for-the-badge)
[![Security and Tests](https://github.com/hack2ai/flask-auth-security/actions/workflows/security.yml/badge.svg)](https://github.com/hack2ai/flask-auth-security/actions/workflows/security.yml)

> A defensive Flask authentication application demonstrating practical secure-coding controls for registration, login, sessions, CSRF protection, password hashing, rate limiting, protected routes, security headers, and automated testing.

## Project status

The application and its security-focused test suite are implemented and documented. The observed GitHub Actions test stage completed with **5 passing tests**. The CI pipeline also runs Bandit against application code; security findings are treated as actionable review items rather than being hidden by the workflow. The project is educational and has not been represented as a production security audit.

## Security controls

| Control | Implementation |
|---|---|
| Password storage | Werkzeug password hashing with `scrypt` |
| CSRF defense | Flask-WTF / CSRF protection |
| Authentication throttling | Flask-Limiter |
| Session protection | `HttpOnly`, `SameSite=Lax`, configurable `Secure`, 30-minute lifetime |
| Input validation | WTForms validation and password-strength checks |
| Protected resources | Authentication decorator and session validation |
| Security headers | CSP, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` |
| Cache protection | `Cache-Control: no-store` |
| Error handling | Generic unexpected-error response with server-side logging |
| Secret management | `SECRET_KEY` supplied through environment configuration |
| Request-size control | 1 MB maximum request body |
| Automated verification | Pytest + Bandit |

The current implementation establishes these controls in `app.py` and `config.py`. fileciteturn98file0 fileciteturn99file0

## Architecture

```text
                        Browser
                           |
                           v
                  Flask Web Application
                           |
            +--------------+--------------+
            |              |              |
            v              v              v
      Input Validation   CSRF Guard   Rate Limiting
            |              |              |
            +--------------+--------------+
                           |
                           v
                 Authentication Logic
                           |
                  +--------+--------+
                  |                 |
                  v                 v
            Session Security   Password Hashing
                  |                 |
                  +--------+--------+
                           |
                           v
                         SQLite

        CI pipeline: Pytest  →  Bandit  →  GitHub Actions
```

## Authentication flow

```text
Registration
    ↓
Validate username/password
    ↓
Hash password
    ↓
Create user

Login
    ↓
Validate credentials
    ↓
Apply rate limit
    ↓
Create authenticated session
    ↓
Protected dashboard
    ↓
Logout / clear session
```

## Technology stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Web framework | Flask |
| Forms | Flask-WTF / WTForms |
| Rate limiting | Flask-Limiter |
| Password hashing | Werkzeug / scrypt |
| Database | SQLite |
| Configuration | Environment variables + `python-dotenv` |
| Testing | Pytest |
| SAST | Bandit |
| CI | GitHub Actions |
| Frontend | HTML / CSS / Jinja templates |

The repository's dependency file pins compatible major/minor version ranges for Flask, Flask-WTF, Flask-Limiter, Werkzeug, Pytest, Bandit, and python-dotenv. fileciteturn100file0

## Repository structure

```text
flask-auth-security/
├── .github/
│   └── workflows/
│       └── security.yml
├── database/
├── static/
├── templates/
├── tests/
├── evidence/
│   ├── README.md
│   └── verified-results.md
├── .env.example
├── .gitignore
├── app.py
├── config.py
├── requirements.txt
├── test_register.py
├── test_security_suite.py
├── bandit-report.txt
├── SECURITY.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

The repository currently contains both the main `tests/` suite and dedicated security-oriented test scripts. fileciteturn96file0

## Getting started

### 1. Clone

```bash
git clone https://github.com/hack2ai/flask-auth-security.git
cd flask-auth-security
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment using the command appropriate for your shell.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the application

Create a local `.env` file from `.env.example` and set a strong development secret. Never commit the real `.env` file.

```text
SECRET_KEY=replace-with-a-local-secret
```

The application intentionally raises an error when `SECRET_KEY` is missing. fileciteturn99file0

### 5. Run

```bash
python app.py
```

The application starts the Flask development server on `127.0.0.1:5000` with debug mode disabled. fileciteturn98file0

## Testing

Run the automated suite with a test-only secret:

```bash
SECRET_KEY=test-secret-key pytest -q
```

The observed CI run reached the test stage successfully with:

```text
5 passed
```

Run the security scanner against application code:

```bash
bandit -r app.py config.py database
```

The repository also includes a previously recorded Bandit report showing no issues in that historical scan; the current CI workflow performs a fresh scan and should be treated as the authoritative current result. fileciteturn103file0

## CI

GitHub Actions runs the following pipeline for relevant changes:

```text
Install dependencies
        ↓
   Pytest suite
        ↓
 Bandit application scan
```

The workflow uses a CI-only secret and CI database path so tests do not depend on production configuration. The workflow file is `.github/workflows/security.yml`.

## Evidence

See [`evidence/README.md`](evidence/README.md) and [`evidence/verified-results.md`](evidence/verified-results.md) for the verification baseline and evidence policy.

Screenshots should only be added after sanitizing credentials, cookies, personal data, and sensitive environment details.

## Security engineering notes

This project demonstrates defensive application-security patterns, but it is **not a production-ready authentication service and has not undergone a formal security audit**.

A real deployment should additionally consider HTTPS enforcement, production secret management and rotation, a production-grade database, MFA where appropriate, account recovery controls, centralized audit logging, dependency and container scanning, monitoring/alerting, authorization design, threat modeling, and penetration testing.

## Responsible testing

Run security testing only against systems and accounts you own or are explicitly authorized to assess. Never place real credentials or production session data into test fixtures.

## Author

**Pankaj (Tony) Kumar**  
AI Engineer • Full Stack Developer • Generative AI & RAG Specialist

[GitHub](https://github.com/hack2ai) • [LinkedIn](https://www.linkedin.com/in/pankaj-kumar-ab591a216)

## License

See [`LICENSE`](LICENSE) for the repository license.