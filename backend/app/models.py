from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

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


class Task(db.Model):
    """Represents a single kanban task."""

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="todo")
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