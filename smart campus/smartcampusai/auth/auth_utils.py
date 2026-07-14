"""
SmartCampusAI — Authentication Utilities
==========================================
Handles user registration, login, session management,
and credential validation with bcrypt security.
"""

import re
import datetime
from typing import Optional
import bcrypt
import streamlit as st
from database.db_utils import find_user, add_user



# ── Password Hashing ──────────────────────────────────────────

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt with a random salt.

    Args:
        password (str): The plaintext password to hash.
    Returns:
        str: The bcrypt hash string.
    """
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """
    Verifies a plaintext password against a stored bcrypt hash.

    Args:
        password (str): The plaintext password to check.
        hashed (str): The stored bcrypt hash.
    Returns:
        bool: True if they match, False otherwise.
    """
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


# ── Validators ────────────────────────────────────────────────

def validate_email(email: str) -> bool:
    """
    Validates email format using a standard RFC-compatible regex.

    Args:
        email (str): Email address string to validate.
    Returns:
        bool: True if valid format, False otherwise.
    """
    pattern = r"^[\w\.\+\-]+@[\w\-]+\.[\w\.\-]+$"
    return bool(re.match(pattern, email.strip()))


def validate_username(username: str) -> tuple[bool, str]:
    """
    Validates that a username meets minimum requirements.

    Args:
        username (str): Username string to validate.
    Returns:
        tuple (bool, str): (is_valid, error_message)
    """
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 30:
        return False, "Username cannot exceed 30 characters."
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, ""


# ── Registration ──────────────────────────────────────────────

def register_user(username: str, email: str, password: str, confirm_password: str) -> tuple[bool, str]:
    """
    Validates input and registers a new user in the JSON database.

    Args:
        username (str): Desired username.
        email (str): Email address.
        password (str): Desired password.
        confirm_password (str): Password confirmation.
    Returns:
        tuple (bool, str): (success, message)
    """
    username = username.strip()
    email    = email.strip()

    # ── Field presence check ──────────────────────────────────
    if not username or not email or not password or not confirm_password:
        return False, "⚠️ All fields are required."

    # ── Username validation ───────────────────────────────────
    valid, err = validate_username(username)
    if not valid:
        return False, f"⚠️ {err}"

    # ── Email validation ──────────────────────────────────────
    if not validate_email(email):
        return False, "⚠️ Please enter a valid email address."

    # ── Password match ────────────────────────────────────────
    if password != confirm_password:
        return False, "⚠️ Passwords do not match."

    # ── Password strength ─────────────────────────────────────
    if len(password) < 6:
        return False, "⚠️ Password must be at least 6 characters long."

    # ── Build user record ─────────────────────────────────────
    user_record = {
        "username":      username,
        "email":         email,
        "password_hash": hash_password(password),
        "role":          "student",
        "created_at":    datetime.datetime.now().isoformat()
    }

    try:
        add_user(user_record)
        return True, f"✅ Account created successfully! Welcome, {username}."
    except ValueError as e:
        return False, f"⚠️ {e}"
    except Exception as e:
        return False, f"❌ An unexpected error occurred: {e}"


# ── Login ─────────────────────────────────────────────────────

def login_user(username_or_email: str, password: str) -> tuple[bool, str]:
    """
    Authenticates user credentials and initializes Streamlit session.

    Args:
        username_or_email (str): Username or email to authenticate.
        password (str): Plaintext password to verify.
    Returns:
        tuple (bool, str): (success, message)
    """
    username_or_email = username_or_email.strip()

    if not username_or_email or not password:
        return False, "⚠️ Please fill in all fields."

    user = find_user(username_or_email)
    if not user:
        return False, "❌ Invalid username/email or password."

    if verify_password(password, user["password_hash"]):
        # Store minimal user info in session state
        st.session_state["user"] = {
            "username":   user["username"],
            "email":      user["email"],
            "role":       user.get("role", "student"),
            "created_at": user["created_at"]
        }
        st.session_state["logged_in"] = True
        return True, f"🚀 Welcome back, {user['username']}!"

    return False, "❌ Invalid username/email or password."


# ── Session Management ────────────────────────────────────────

def logout_user() -> None:
    """Clears all active Streamlit session state keys."""
    st.session_state.clear()


def is_logged_in() -> bool:
    """
    Checks whether a valid user session exists.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    return (
        st.session_state.get("logged_in", False)
        and "user" in st.session_state
        and isinstance(st.session_state["user"], dict)
    )


def get_current_user() ->  Optional[dict]:
    """
    Retrieves the currently logged-in user from session state.

    Returns:
        dict | None: The user dict if logged in, else None.
    """
    if is_logged_in():
        return st.session_state.get("user")
    return None
