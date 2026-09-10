from flask import Blueprint, jsonify, request

from app.models import STATUSES, Task, db

tasks_bp = Blueprint("tasks", __name__)


def error_response(message, code):
    return jsonify({"error": message}), code


def cleaned_text(value):
    """Return the trimmed string or None if value is missing/blank."""
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value if value else None


def validate_status(value):
    return value in STATUSES


@tasks_bp.get("/tasks")
def get_tasks():
    """GET /api/tasks -> fetch all tasks from the database."""
    tasks = Task.query.order_by(Task.created_at.desc(), Task.id.desc()).all()
    return jsonify({"tasks": [task.to_dict() for task in tasks]})


@tasks_bp.post("/tasks")
def create_task():
    """POST /api/tasks -> create a task with status 'todo'."""
    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return error_response("Request body must be valid JSON", 400)

    title = cleaned_text(data.get("title"))
    description = cleaned_text(data.get("description"))

    if not title:
        return error_response("Title is required", 400)
    if not description:
        return error_response("Description is required", 400)

    task = Task(title=title, description=description, status="todo")
    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@tasks_bp.put("/tasks/<int:task_id>")
def update_task(task_id):
    """PUT /api/tasks/<id> -> update title, description and/or status."""
    task = db.session.get(Task, task_id)
    if task is None:
        return error_response("Task not found", 404)

    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return error_response("Request body must be valid JSON", 400)

    if not data:
        return error_response("No fields to update", 400)

    if "title" in data:
        title = cleaned_text(data.get("title"))
        if not title:
            return error_response("Title is required", 400)
        task.title = title

    if "description" in data:
        description = cleaned_text(data.get("description"))
        if not description:
            return error_response("Description is required", 400)
        task.description = description

    if "status" in data:
        status = data.get("status")
        if status not in STATUSES:
            return error_response(
                "Invalid status. Allowed values: todo, in_progress, done", 400
            )
        task.status = status

    db.session.commit()
    return jsonify(task.to_dict())


@tasks_bp.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    """DELETE /api/tasks/<id> -> permanently delete a task."""
    task = db.session.get(Task, task_id)
    if task is None:
        return error_response("Task not found", 404)

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"Task {task_id} deleted"})