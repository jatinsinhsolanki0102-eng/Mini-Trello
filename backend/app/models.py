from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


def _utcnow():
    """Naive UTC datetime (avoids deprecated datetime.utcnow)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

# Allowed status values for a task.
STATUSES = ["todo", "in_progress", "done"]

# Valid status transitions for the kanban flow.
VALID_TRANSITIONS = {
    "todo": ("in_progress",),
    "in_progress": ("todo", "done"),
    "done": ("in_progress",),
}


class User(db.Model):
    """An account that owns its own private kanban board."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow)

    tasks = db.relationship("Task", backref="owner", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "username": self.username}


class Task(db.Model):
    """Represents a single kanban task, owned by a user."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="todo")
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('todo', 'in_progress', 'done')",
            name="ck_task_status",
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            ),
        }

    def __repr__(self):
        return f"<Task {self.id}: {self.title} [{self.status}]>"