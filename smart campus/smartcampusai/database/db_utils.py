"""
SmartCampusAI — JSON Database Utilities
========================================
Thread-safe and process-safe JSON database operations using file-level locking.
Manages users, events, and announcements in a flat-file JSON format.
"""

import os
import json
import time
from contextlib import contextmanager
from typing import Optional

# ── Database file paths (relative to this file's directory) ──
BASE_DIR = os.path.dirname(__file__)

USERS_FILE        = os.path.join(BASE_DIR, "users.json")
EVENTS_FILE       = os.path.join(BASE_DIR, "events.json")
ANNOUNCEMENTS_FILE= os.path.join(BASE_DIR, "announcements.json")

# ── File Lock Helpers ─────────────────────────────────────────

@contextmanager
def db_lock(lock_path: str, timeout: float = 5.0):
    """
    Cross-platform file lock using exclusive OS-level file creation.
    Prevents concurrent reads/writes from corrupting JSON data.

    Args:
        lock_path (str): Path to the lock file.
        timeout (float): Max seconds to wait before raising RuntimeError.
    """
    deadline = time.monotonic() + timeout
    while True:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            if time.monotonic() > deadline:
                raise RuntimeError(f"Database lock timed out for: {lock_path}")
            time.sleep(0.05)
    try:
        yield
    finally:
        try:
            os.remove(lock_path)
        except FileNotFoundError:
            pass


def _load_json(filepath: str) -> list:
    """Generic JSON file loader with lock-safety."""
    if not os.path.exists(filepath):
        return []
    lock_path = filepath + ".lock"
    with db_lock(lock_path):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return []


def _save_json(filepath: str, data: list) -> None:
    """Generic JSON file writer with lock-safety."""
    lock_path = filepath + ".lock"
    with db_lock(lock_path):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


# ── User Operations ───────────────────────────────────────────

def load_users() -> list:
    """Returns all registered users from the JSON database."""
    return _load_json(USERS_FILE)


def save_users(users: list) -> None:
    """Persists the full user list to the JSON database."""
    _save_json(USERS_FILE, users)


def find_user(username_or_email: str) -> Optional[dict]:
    """
    Searches for a user by username or email (case-insensitive).

    Args:
        username_or_email (str): The search query.
    Returns:
        dict | None: The matching user record, or None.
    """
    query = username_or_email.strip().lower()
    for user in load_users():
        if user.get("username", "").lower() == query:
            return user
        if user.get("email", "").lower() == query:
            return user
    return None


def add_user(user_dict: dict) -> None:
    """
    Adds a new user to the database after uniqueness validation.

    Args:
        user_dict (dict): User record with username, email, password_hash, created_at.
    Raises:
        ValueError: If username or email already exists.
    """
    users = load_users()
    new_username = user_dict["username"].strip().lower()
    new_email    = user_dict["email"].strip().lower()

    for existing in users:
        if existing.get("username", "").lower() == new_username:
            raise ValueError("Username is already taken. Please choose another.")
        if existing.get("email", "").lower() == new_email:
            raise ValueError("Email address is already registered. Try logging in.")

    users.append(user_dict)
    save_users(users)


# ── Events Operations ─────────────────────────────────────────

def load_events() -> list:
    """Returns all campus events from the JSON database."""
    return _load_json(EVENTS_FILE)


# ── Announcements Operations ──────────────────────────────────

def load_announcements() -> list:
    """Returns all campus announcements from the JSON database."""
    return _load_json(ANNOUNCEMENTS_FILE)
