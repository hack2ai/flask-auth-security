# Security Policy

## Scope

This repository is an educational secure-coding project demonstrating defensive Flask authentication controls. It is not represented as a production security audit or certification.

## Supported branch

Security fixes should target the current `main` branch unless a maintained release branch is explicitly documented.

## Reporting a security issue

Please do not publish credentials, session cookies, private user data, or sensitive proof-of-concept details in a public issue.

For a vulnerability in the repository, use GitHub's private vulnerability reporting/security advisory features when available. Provide enough information to reproduce the problem safely, including affected files, expected behavior, observed behavior, and impact.

## Security design notes

The application currently demonstrates controls including password hashing, CSRF protection, authentication rate limiting, protected routes, secure cookie settings, content-security policy and related security headers, input validation, and automated security tests.

Configuration requires a `SECRET_KEY` supplied through the environment; do not commit real secrets. Production deployments should use HTTPS, secure secret management, a production-ready database, monitoring, and a deployment architecture appropriate for the application's threat model.

## Safe testing

Test only systems and accounts you own or are explicitly authorized to assess. Avoid placing real credentials, personal information, or production session data in test fixtures or repository files.
