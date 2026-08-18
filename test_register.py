import re

from app import create_app
from config import TestingConfig
from database.db import get_user_by_username

app = create_app(TestingConfig())

with app.test_client() as client:
    # 1. GET registration page
    response = client.get("/register")

    print("REGISTER GET:", response.status_code)

    html = response.data.decode()

    # 2. Extract CSRF token
    match = re.search(
        r'name="csrf_token"[^>]*value="([^"]+)"',
        html
    )

    print("CSRF TOKEN FOUND:", bool(match))

    if not match:
        print("ERROR: CSRF token was not found.")
        raise SystemExit(1)

    csrf_token = match.group(1)

    # 3. Submit registration
    response = client.post(
        "/register",
        data={
            "csrf_token": csrf_token,
            "username": "securitytest02",
            "password": "SecureTest@12345",
        },
        follow_redirects=False,
    )

    print("REGISTER POST:", response.status_code)
    print("REGISTER LOCATION:", response.headers.get("Location"))

    # 4. Verify user exists in database
    with app.app_context():
        user = get_user_by_username("securitytest02")

        print("USER CREATED:", user is not None)

        if user:
            print("USERNAME:", user["username"])
            print("PASSWORD HASH EXISTS:", bool(user["password_hash"]))
