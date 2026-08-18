# Secure Flask Authentication System

A security-focused Flask web application demonstrating secure user authentication, session management, CSRF protection, password hashing, rate limiting, protected routes, and HTTP security headers.

This project was developed and tested in an isolated Kali Linux environment as a practical secure-coding and web-application-security project.

---

## 1. Project Overview

The Secure Flask Authentication System provides a protected authentication workflow consisting of:

- User registration
- User login
- User logout
- Password hashing
- Session-based authentication
- CSRF protection
- Protected dashboard
- Authentication rate limiting
- Security response headers
- Automated security testing

The primary goal of the project is to demonstrate how common authentication vulnerabilities can be mitigated using Flask security mechanisms and secure coding practices.

---

## 2. Project Objectives

The main objectives are:

1. Implement secure user authentication.
2. Prevent unauthorized access to protected resources.
3. Protect authentication forms against CSRF attacks.
4. Store passwords using secure password hashing.
5. Implement session-based authentication.
6. Prevent excessive login attempts using rate limiting.
7. Add HTTP security response headers.
8. Automatically test important security controls.
9. Verify that logout invalidates authenticated sessions.
10. Produce reproducible security-test evidence.

---

## 3. Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| Web Framework | Flask |
| Authentication | Session-based authentication |
| Password Security | Password hashing |
| CSRF Protection | Flask-WTF / CSRF protection |
| Database | SQLite |
| Frontend | HTML / CSS |
| Operating System | Kali Linux |
| Testing | Python security test suite |

---

## 4. Security Features

### 4.1 Password Hashing

Passwords are not stored as plaintext.

The application uses password hashing so that the original password is not directly stored in the database.

Benefits:

- Prevents plaintext password storage.
- Reduces damage from database exposure.
- Makes password verification safer.

---

### 4.2 Session-Based Authentication

After successful authentication, the application creates an authenticated session.

Protected routes verify the authentication state before allowing access.

Example protected endpoint:

```text
/dashboard
