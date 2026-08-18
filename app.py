import re
from functools import wraps

from dotenv import load_dotenv

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    session,
    url_for,
)

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect

from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash, generate_password_hash

from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Regexp,
    ValidationError,
)

from config import Config, TestingConfig

from database.db import (
    create_user,
    get_user_by_id,
    get_user_by_username,
    init_db,
)


# ============================================================
# Environment
# ============================================================

load_dotenv()


# ============================================================
# Extensions
# ============================================================

csrf = CSRFProtect()


# ============================================================
# Application Factory
# ============================================================

def create_app(test_config=None):
    app = Flask(__name__)

    # --------------------------------------------------------
    # Configuration
    # --------------------------------------------------------

    if test_config is None:
        app.config.from_object(Config)
    else:
        if isinstance(test_config, dict):
            app.config.from_mapping(test_config)
        else:
            app.config.from_object(test_config)

    # --------------------------------------------------------
    # CSRF protection
    # --------------------------------------------------------

    csrf.init_app(app)

    # --------------------------------------------------------
    # Rate limiting
    # --------------------------------------------------------

    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=[
            "200 per day",
            "50 per hour",
        ],
        storage_uri="memory://",
    )

    # ========================================================
    # Security Headers
    # ========================================================

    @app.after_request
    def add_security_headers(response):
        # Do not expose server information.
        response.headers.pop("Server", None)

        # Prevent MIME-type sniffing.
        response.headers.setdefault(
            "X-Content-Type-Options",
            "nosniff",
        )

        # Prevent the page from being embedded in frames.
        response.headers.setdefault(
            "X-Frame-Options",
            "DENY",
        )

        # Control referrer information.
        response.headers.setdefault(
            "Referrer-Policy",
            "strict-origin-when-cross-origin",
        )
        # Restrict access to sensitive browser features.
        response.headers.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
        )

        # Basic Content Security Policy.
        response.headers.setdefault(
            "Content-Security-Policy",
            (
                "default-src 'self'; "
                "style-src 'self'; "
                "script-src 'self'; "
                "img-src 'self' data:; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "frame-ancestors 'none'; "
                "form-action 'self';"
            ),
        )

        # Prevent caching of authenticated pages.
        response.headers.setdefault(
            "Cache-Control",
            "no-store",
        )

        return response

    # ========================================================
    # Error Handling
    # ========================================================

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """
        Handle unexpected application errors.
        """

        # Let Flask handle normal HTTP exceptions
        # such as 400, 403, 404, etc.
        if isinstance(error, HTTPException):
            return error

        app.logger.exception(
            "Unhandled application exception"
        )

        return (
            render_template(
                "base.html",
                error_message="An unexpected error occurred.",
            ),
            500,
        )

    @app.errorhandler(404)
    def page_not_found(error):
        """
        Handle missing routes/pages.
        """

        return (
            render_template(
                "base.html",
                error_message="The requested page was not found.",
            ),
            404,
        )

    # ========================================================
    # Authentication Forms
    # ========================================================

    class RegistrationForm(FlaskForm):
        username = StringField(
            "Username",
            validators=[
                DataRequired(),
                Length(min=3, max=30),
                Regexp(
                    r"^[A-Za-z0-9_.-]+$",
                    message=(
                        "Use only letters, numbers, "
                        "'.', '_' and '-'."
                    ),
                ),
            ],
        )

        password = PasswordField(
            "Password",
            validators=[
                DataRequired(),
                Length(min=12, max=128),
            ],
        )

        submit = SubmitField("Register")

        def validate_password(self, field):
            """
            Enforce a strong password policy.
            """

            password = field.data

            if not re.search(r"[A-Z]", password):
                raise ValidationError(
                    "Password must contain an uppercase letter."
                )

            if not re.search(r"[a-z]", password):
                raise ValidationError(
                    "Password must contain a lowercase letter."
                )

            if not re.search(r"\d", password):
                raise ValidationError(
                    "Password must contain a number."
                )

            if not re.search(r"[^A-Za-z0-9]", password):
                raise ValidationError(
                    "Password must contain a special character."
                )

    class LoginForm(FlaskForm):
        username = StringField(
            "Username",
            validators=[
                DataRequired(),
                Length(min=3, max=30),
            ],
        )

        password = PasswordField(
            "Password",
            validators=[
                DataRequired(),
                Length(max=128),
            ],
        )

        submit = SubmitField("Login")

    class LogoutForm(FlaskForm):
        submit = SubmitField("Logout")

    # ========================================================
    # Authentication Decorator
    # ========================================================

    def login_required(view_function):
        """
        Protect routes that require an authenticated user.
        """

        @wraps(view_function)
        def wrapped_view(*args, **kwargs):
            user_id = session.get("user_id")

            if user_id is None:
                return redirect(url_for("login"))

            user = get_user_by_id(user_id)

            if user is None:
                session.clear()
                return redirect(url_for("login"))

            return view_function(*args, **kwargs)

        return wrapped_view

    # ========================================================
    # Routes
    # ========================================================

    @app.route("/")
    def index():
        """
        Redirect authenticated users to dashboard,
        otherwise redirect to login.
        """

        if session.get("user_id"):
            return redirect(url_for("dashboard"))

        return redirect(url_for("login"))

    # ========================================================
    # Registration
    # ========================================================

    @app.route(
        "/register",
        methods=["GET", "POST"],
    )
    @limiter.limit("5 per minute")
    def register():
        form = RegistrationForm()

        if form.validate_on_submit():
            username = form.username.data.strip()
            password = form.password.data

            # Check whether username already exists.
            existing_user = get_user_by_username(username)

            if existing_user:
                form.username.errors.append(
                    "Unable to create this account. "
                    "Choose another username."
                )

                return render_template(
                    "register.html",
                    form=form,
                )

            # Hash password using scrypt.
            password_hash = generate_password_hash(
                password,
                method="scrypt",
            )

            # Create user.
            create_user(
                username,
                password_hash,
            )

            return redirect(url_for("login"))

        return render_template(
            "register.html",
            form=form,
        )

    # ========================================================
    # Login
    # ========================================================

    @app.route(
        "/login",
        methods=["GET", "POST"],
    )
    @limiter.limit("5 per minute")
    def login():
        form = LoginForm()

        if form.validate_on_submit():
            username = form.username.data.strip()
            password = form.password.data

            user = get_user_by_username(username)


            if user is not None:
                password_matches = check_password_hash(
                    user["password_hash"],
                    password
                )

            else:
                password_matches = False

            # Generic authentication failure message.
            if user is None or not password_matches:
                form.password.errors.append(
                    "Invalid username or password."
                )

                return (
                    render_template(
                        "login.html",
                        form=form,
                    ),
                    401,
                )	

            # ------------------------------------------------
            # Establish authenticated session
            # ------------------------------------------------

            session.clear()

            session.permanent = True

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(
                url_for("dashboard")
            )

        return render_template(
            "login.html",
            form=form,
        )

    # ========================================================
    # Logout
    # ========================================================

  

    @app.route("/logout", methods=["GET", "POST"])
    @login_required
    def logout():
        form = LogoutForm()
    
        if form.validate_on_submit():
            session.clear()
            return redirect(url_for("login"))
    
        return render_template(
            "logout.html",
            form=form,
        )
    
        # ========================================================
    # Protected Dashboard
    # ========================================================

    @app.route("/dashboard")
    @login_required
    def dashboard():
        user_id = session.get("user_id")

        user = get_user_by_id(user_id)

        # The user could have been deleted after login.
        if user is None:
            session.clear()

            return redirect(
                url_for("login")
            )

        return render_template(
            "dashboard.html",
            user=user,
            logout_form=LogoutForm(),
        )

    # ========================================================
    # Database Initialization
    # ========================================================

    with app.app_context():
        init_db()

    return app


# ============================================================
# Development Server
# ============================================================

if __name__ == "__main__":
    application = create_app()

    # Development server only.
    # Debug mode intentionally disabled.
    application.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
    )
