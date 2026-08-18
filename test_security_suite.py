import re

from app import create_app
from config import TestingConfig


USERNAME = "securitytest02"
PASSWORD = "SecureTest012345"
WRONG_PASSWORD = "DefinitelyWrongPassword123!"


def get_csrf_token(client):
    response = client.get("/login")

    html = response.data.decode()

    match = re.search(
        r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']',
        html
    )

    return response, match.group(1) if match else None


def check(name, condition):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}")
    return condition


app = create_app(TestingConfig())

results = []

with app.test_client() as client:

    print("\n========================================")
    print(" FLASK AUTHENTICATION SECURITY SUITE")
    print("========================================\n")

    # ----------------------------------------
    # 1. Login page + CSRF
    # ----------------------------------------

    response, csrf_token = get_csrf_token(client)

    results.append(
        check(
            "Login page returns HTTP 200",
            response.status_code == 200
        )
    )

    results.append(
        check(
            "CSRF token is present",
            csrf_token is not None
        )
    )

    if not csrf_token:
        print("\nCSRF token could not be obtained.")
        print("Stopping test suite.")
        raise SystemExit(1)

    # ----------------------------------------
    # 2. Invalid login
    # ----------------------------------------

    response = client.post(
        "/login",
        data={
            "csrf_token": csrf_token,
            "username": USERNAME,
            "password": WRONG_PASSWORD,
        },
        follow_redirects=False,
    )

    results.append(
        check(
            "Invalid credentials return HTTP 401",
            response.status_code == 401
        )
    )

    # ----------------------------------------
    # 3. Valid login
    # ----------------------------------------

    response = client.post(
        "/login",
        data={
            "csrf_token": csrf_token,
            "username": USERNAME,
            "password": PASSWORD,
        },
        follow_redirects=False,
    )

    results.append(
        check(
            "Valid login redirects to dashboard",
            response.status_code == 302
            and response.headers.get("Location") == "/dashboard"
        )
    )

    # ----------------------------------------
    # 4. Protected dashboard
    # ----------------------------------------

    response = client.get(
        "/dashboard",
        follow_redirects=False
    )

    results.append(
        check(
            "Authenticated user can access dashboard",
            response.status_code == 200
        )
    )

    # ----------------------------------------
    # 5. Logout page
    # ----------------------------------------

    response = client.get("/logout")

    logout_html = response.data.decode()

    logout_match = re.search(
        r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']',
        logout_html
    )

    logout_csrf = (
        logout_match.group(1)
        if logout_match
        else None
    )

    results.append(
        check(
            "Logout page returns HTTP 200",
            response.status_code == 200
        )
    )

    results.append(
        check(
            "Logout CSRF token is present",
            logout_csrf is not None
        )
    )

    # ----------------------------------------
    # 6. Logout with valid CSRF
    # ----------------------------------------

    if logout_csrf:

        response = client.post(
            "/logout",
            data={
                "csrf_token": logout_csrf,
                "submit": "Logout",
            },
            follow_redirects=False,
        )

        results.append(
            check(
                "Valid logout redirects to login",
                response.status_code == 302
                and response.headers.get("Location") == "/login"
            )
        )

    # ----------------------------------------
    # 7. Dashboard blocked after logout
    # ----------------------------------------

    response = client.get(
        "/dashboard",
        follow_redirects=False
    )

    results.append(
        check(
            "Dashboard blocked after logout",
            response.status_code == 302
            and response.headers.get("Location") == "/login"
        )
    )

    # ----------------------------------------
    # 8. Security headers
    # ----------------------------------------

    response = client.get("/login")

    results.append(
        check(
            "X-Content-Type-Options is nosniff",
            response.headers.get("X-Content-Type-Options")
            == "nosniff"
        )
    )

    results.append(
        check(
            "X-Frame-Options is DENY",
            response.headers.get("X-Frame-Options")
            == "DENY"
        )
    )

    results.append(
        check(
            "Content-Security-Policy is present",
            bool(response.headers.get("Content-Security-Policy"))
        )
    )

    results.append(
        check(
            "Referrer-Policy is present",
            bool(response.headers.get("Referrer-Policy"))
        )
    )

    results.append(
        check(
            "Permissions-Policy is present",
            bool(response.headers.get("Permissions-Policy"))
        )
    )

    # ----------------------------------------
    # 9. Rate limiting
    # ----------------------------------------

    response, csrf_token = get_csrf_token(client)

    rate_limit_triggered = False

    for attempt in range(1, 11):

        response = client.post(
            "/login",
            data={
                "csrf_token": csrf_token,
                "username": USERNAME,
                "password": WRONG_PASSWORD,
            },
            follow_redirects=False,
        )

        print(
            f"Rate-limit attempt {attempt}: "
            f"{response.status_code}"
        )

        if response.status_code == 429:
            rate_limit_triggered = True
            break

    results.append(
        check(
            "Login rate limiting returns HTTP 429",
            rate_limit_triggered
        )
    )


# ----------------------------------------
# Final summary
# ----------------------------------------

passed = sum(results)
total = len(results)
failed = total - passed

print("\n========================================")
print(" SECURITY TEST SUMMARY")
print("========================================")

print(f"TOTAL TESTS : {total}")
print(f"PASSED      : {passed}")
print(f"FAILED      : {failed}")

if failed == 0:
    print("\nRESULT: ALL SECURITY TESTS PASSED")
else:
    print("\nRESULT: SOME SECURITY TESTS FAILED")

print("========================================")
