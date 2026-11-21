import os
import sqlite3
from datetime import datetime, timezone
from functools import wraps

from flask import Flask, abort, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-demo-only-change-me")
DATABASE = os.environ.get("DATABASE", "accesscheck.db")

# Fictional users for the local demo. Do not use these as real accounts.
USERS = {
    "alex": {"name": "Alex Demo", "role": "viewer", "mfa": True},
    "sam": {"name": "Sam Demo", "role": "admin", "mfa": False},
    "jordan": {"name": "Jordan Demo", "role": "admin", "mfa": True},
}


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                action TEXT NOT NULL,
                decision TEXT NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def record_event(user_name, action, decision, reason):
    with get_db() as db:
        db.execute(
            """INSERT INTO audit_log
               (user_name, action, decision, reason, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (
                user_name,
                action,
                decision,
                reason,
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
            ),
        )


def current_user():
    user_id = session.get("user_id")
    if user_id not in USERS:
        return None
    return USERS[user_id]


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for("index"))
        return view(*args, **kwargs)
    return wrapped


@app.get("/")
def index():
    return render_template("index.html", users=USERS)


@app.post("/demo-login")
def demo_login():
    user_id = request.form.get("user_id", "")
    if user_id not in USERS:
        abort(400, "Unknown demo user.")

    session.clear()
    session["user_id"] = user_id
    return redirect(url_for("dashboard"))


@app.get("/dashboard")
@login_required
def dashboard():
    user = current_user()
    with get_db() as db:
        events = db.execute(
            "SELECT * FROM audit_log ORDER BY id DESC LIMIT 10"
        ).fetchall()

    return render_template("dashboard.html", user=user, events=events)


@app.post("/sensitive-action")
@login_required
def sensitive_action():
    user = current_user()

    # The policy deliberately ignores IP address and VPN location.
    if user["role"] != "admin":
        decision, reason = "DENIED", "Admin role required."
    elif not user["mfa"]:
        decision, reason = "DENIED", "MFA is required for this action."
    else:
        decision, reason = "ALLOWED", "Admin role and MFA requirements met."

    record_event(user["name"], "Sensitive demo action", decision, reason)
    return redirect(url_for("dashboard"))


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    # Local development only. Do not expose Flask's development server publicly.
    app.run(debug=True)
