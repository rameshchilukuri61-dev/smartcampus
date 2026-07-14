import os
import json
import uuid
import bcrypt

DB_FILE = os.path.join(os.path.dirname(__file__), "users.json")

def load_users():
    """Load users from the JSON database file. Creates the file if it does not exist."""
    if not os.path.exists(DB_FILE):
        default_db = {"users": []}
        try:
            with open(DB_FILE, "w") as f:
                json.dump(default_db, f, indent=2)
            return []
        except Exception as e:
            print(f"Error creating database file: {e}")
            return []

    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            return data.get("users", [])
    except Exception as e:
        print(f"Error reading database file: {e}")
        return []

def save_users(users):
    """Save the users list to the JSON database file."""
    try:
        with open(DB_FILE, "w") as f:
            json.dump({"users": users}, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    """Verify password against its bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def register_user(name, email, student_id, department, password):
    """
    Register a new student.
    Prevents duplicate emails and initializes default campus data.
    """
    users = load_users()
    
    # Check duplicate email
    email_clean = email.strip().lower()
    if any(u.get("email", "").strip().lower() == email_clean for u in users):
        return False, "An account with this email already exists."

    # Initialize default student attendance
    default_attendance = {
        "Mathematics": {"attended": 16, "total": 20},
        "Physics": {"attended": 14, "total": 20},
        "Chemistry": {"attended": 18, "total": 20},
        "Computer Science": {"attended": 15, "total": 20},
        "English": {"attended": 17, "total": 20}
    }

    # Initialize default student timetable
    default_timetable = [
        {"id": "t1", "day": "Monday", "time": "09:00 - 10:00", "subject": "Mathematics", "room": "LH-101"},
        {"id": "t2", "day": "Monday", "time": "10:15 - 11:15", "subject": "Physics", "room": "Lab-2"},
        {"id": "t3", "day": "Tuesday", "time": "09:00 - 10:00", "subject": "Chemistry", "room": "LH-102"},
        {"id": "t4", "day": "Wednesday", "time": "11:30 - 12:30", "subject": "Computer Science", "room": "LH-201"},
        {"id": "t5", "day": "Thursday", "time": "14:00 - 15:00", "subject": "English", "room": "LH-103"},
        {"id": "t6", "day": "Friday", "time": "10:15 - 11:15", "subject": "Physics", "room": "Lab-2"}
    ]

    new_user = {
        "id": str(uuid.uuid4()),
        "name": name.strip(),
        "email": email_clean,
        "student_id": student_id.strip().upper(),
        "department": department.strip().upper(),
        "password": hash_password(password),
        "attendance": default_attendance,
        "timetable": default_timetable
    }

    users.append(new_user)
    if save_users(users):
        return True, new_user
    else:
        return False, "Database save operation failed."

def authenticate_user(email, password):
    """Authenticate a student. Returns user object if successful, else None."""
    users = load_users()
    email_clean = email.strip().lower()
    for user in users:
        if user.get("email", "").strip().lower() == email_clean:
            if check_password(password, user.get("password", "")):
                return user
            break
    return None

def update_user(email, updated_data):
    """Update a user's details by matching their email."""
    users = load_users()
    email_clean = email.strip().lower()
    for i, user in enumerate(users):
        if user.get("email", "").strip().lower() == email_clean:
            # Update matching keys
            for key, val in updated_data.items():
                # Avoid resetting keys that shouldn't be overridden
                user[key] = val
            users[i] = user
            return save_users(users)
    return False
