# Contributing

Thank you for contributing to `flask-auth-security`.

## Scope

Contributions should improve the application's secure-coding examples, authentication behavior, tests, documentation, or development workflow.

## Before contributing

- Never commit real passwords, API keys, session cookies, `.env` files, databases, or private user data.
- Use local/test-only credentials and isolated test databases.
- Keep security claims limited to behavior that has actually been tested.

## Development workflow

Create a virtual environment and install the repository dependencies:

```bash
python -m venv venv
# Activate the environment for your shell
pip install -r requirements.txt
```

Set a local development secret before starting the application:

```bash
# Linux/macOS
export SECRET_KEY="replace-with-a-local-secret"
python app.py
```

## Testing

Run the test suite before submitting a change:

```bash
SECRET_KEY=test-secret-key pytest -q
```

Run the security scanner against application code:

```bash
bandit -r app.py config.py database
```

GitHub Actions runs the automated test and security checks for relevant changes.

## Security changes

For authentication or security-control changes, explain:

- the threat or failure mode addressed
- the defensive control changed
- the tests that cover the change
- any deployment limitations or assumptions

Do not weaken production security controls merely to make tests pass; use an explicit test configuration instead.

## Pull requests

A pull request should contain a concise summary, motivation, testing results, and documentation updates when behavior changes.

## Reporting security issues

Follow [`SECURITY.md`](SECURITY.md) for security-sensitive reports rather than publishing sensitive details in a public issue.