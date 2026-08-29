# Verification Evidence

This directory documents reproducible security and functional verification for the Flask authentication project.

## Evidence policy

Only sanitized, repository-relevant evidence should be committed. Never include real credentials, session cookies, private user data, `.env` files, production databases, or unrelated logs.

## Recommended evidence

- test-suite output
- security-scan output
- screenshots of authentication flows
- screenshots of security headers or protected-route behavior
- CI workflow results

## Current verified baseline

The repository's automated security suite has been executed in GitHub Actions and the latest observed test stage completed successfully with **5 passed** tests. Bandit is configured separately against application code.

See [`verified-results.md`](verified-results.md) for the evidence summary.