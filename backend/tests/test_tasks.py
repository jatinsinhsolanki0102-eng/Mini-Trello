"""Backend API tests for Mini-Trello."""

VALID_TITLE = "Design Database"
VALID_DESCRIPTION = "Create MySQL schema for tasks"


def _create_task(client, title=VALID_TITLE, description=VALID_DESCRIPTION):
    return client.post("/api/tasks", json={"title": title, "description": description})


# ----------------------------------------------------------- GET tasks


def test_get_empty_database_returns_empty_list(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.get_json() == {"tasks": []}


def test_get_tasks_returns_all_created_tasks(client):
    _create_task(client, "Task A", "Description A")
    _create_task(client, "Task B", "Description B")

    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["tasks"]) == 2
    titles = {task["title"] for task in data["tasks"]}
    assert titles == {"Task A", "Task B"}


# ---------------------------------------------------------- POST task


def test_create_task_returns_201_with_todo_status(client):
    response = _create_task(client)
    assert response.status_code == 201
    body = response.get_json()
    assert body["title"] == VALID_TITLE
    assert body["description"] == VALID_DESCRIPTION
    assert body["status"] == "todo"
    assert isinstance(body["id"], int)


def test_create_task_persists_in_database(client):
    created = _create_task(client).get_json()
    response = client.get("/api/tasks")
    assert len(response.get_json()["tasks"]) == 1
    assert response.get_json()["tasks"][0]["id"] == created["id"]


def test_create_task_trims_whitespace(client):
    response = client.post(
        "/api/tasks",
        json={
            "title": "   Trimmed title   ",
            "description": "   Trimmed description   ",
        },
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body["title"] == "Trimmed title"
    assert body["description"] == "Trimmed description"


# --------------------------------------------------- POST validation


def test_post_empty_title_returns_400(client):
    response = client.post(
        "/api/tasks", json={"title": "", "description": "Something"}
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_post_missing_title_returns_400(client):
    response = client.post("/api/tasks", json={"description": "Something"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_post_whitespace_only_title_returns_400(client):
    response = client.post(
        "/api/tasks", json={"title": "   ", "description": "Something"}
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_post_empty_description_returns_400(client):
    response = client.post(
        "/api/tasks", json={"title": "Create UI", "description": ""}
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Description is required"


def test_post_missing_description_returns_400(client):
    response = client.post("/api/tasks", json={"title": "Create UI"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Description is required"


def test_post_non_json_body_returns_400(client):
    response = client.post("/api/tasks", data="not json", content_type="text/plain")
    assert response.status_code == 400


def test_post_does_not_accept_arbitrary_status(client):
    response = client.post(
        "/api/tasks",
        json={
            "title": "X",
            "description": "Y",
            "status": "done",
        },
    )
    assert response.status_code == 201
    # A new task always starts in "todo", the provided status is ignored.
    assert response.get_json()["status"] == "todo"


# ---------------------------------------------------------- PUT task


def test_update_status_to_in_progress(client):
    task_id = _create_task(client).get_json()["id"]
    response = client.put(f"/api/tasks/{task_id}", json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.get_json()["status"] == "in_progress"


def test_update_status_to_done(client):
    task_id = _create_task(client).get_json()["id"]
    response = client.put(f"/api/tasks/{task_id}", json={"status": "done"})
    assert response.status_code == 200
    assert response.get_json()["status"] == "done"


def test_full_status_transition_sequence(client):
    task_id = _create_task(client).get_json()["id"]

    r1 = client.put(f"/api/tasks/{task_id}", json={"status": "in_progress"})
    assert r1.get_json()["status"] == "in_progress"

    r2 = client.put(f"/api/tasks/{task_id}", json={"status": "done"})
    assert r2.get_json()["status"] == "done"

    r3 = client.put(f"/api/tasks/{task_id}", json={"status": "todo"})
    assert r3.get_json()["status"] == "todo"


def test_update_title_and_description(client):
    task_id = _create_task(client).get_json()["id"]
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "New title", "description": "New description"},
    )
    body = response.get_json()
    assert response.status_code == 200
    assert body["title"] == "New title"
    assert body["description"] == "New description"


# --------------------------------------------------- PUT validation


def test_update_invalid_status_returns_400(client):
    task_id = _create_task(client).get_json()["id"]
    response = client.put(f"/api/tasks/{task_id}", json={"status": "review"})
    assert response.status_code == 400
    assert "Invalid status" in response.get_json()["error"]


def test_update_nonexistent_task_returns_404(client):
    response = client.put("/api/tasks/99999", json={"status": "done"})
    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found"


def test_update_with_empty_title_returns_400(client):
    task_id = _create_task(client).get_json()["id"]
    response = client.put(f"/api/tasks/{task_id}", json={"title": "  "})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_update_with_empty_body_returns_400(client):
    task_id = _create_task(client).get_json()["id"]
    response = client.put(f"/api/tasks/{task_id}", json={})
    assert response.status_code == 400


# -------------------------------------------------------- DELETE task


def test_delete_task_removes_it(client):
    task_id = _create_task(client).get_json()["id"]
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == f"Task {task_id} deleted"

    remaining = client.get("/api/tasks").get_json()["tasks"]
    assert remaining == []


def test_delete_nonexistent_task_returns_404(client):
    response = client.delete("/api/tasks/99999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found"


def test_delete_does_not_affect_other_tasks(client):
    _create_task(client, "Keep me", "description")
    doomed = _create_task(client, "Delete me", "description").get_json()["id"]

    client.delete(f"/api/tasks/{doomed}")

    remaining = client.get("/api/tasks").get_json()["tasks"]
    assert len(remaining) == 1
    assert remaining[0]["title"] == "Keep me"


# ------------------------------------------- columns grouping support


def test_get_returns_tasks_with_all_statuses_for_columns(client):
    t1 = _create_task(client, "To do task", "d").get_json()
    t2 = _create_task(client, "Wip task", "d").get_json()
    t3 = _create_task(client, "Done task", "d").get_json()

    client.put(f"/api/tasks/{t2['id']}", json={"status": "in_progress"})
    client.put(f"/api/tasks/{t3['id']}", json={"status": "done"})

    tasks = client.get("/api/tasks").get_json()["tasks"]
    by_status = {task["id"]: task["status"] for task in tasks}
    assert by_status[t1["id"]] == "todo"
    assert by_status[t2["id"]] == "in_progress"
    assert by_status[t3["id"]] == "done"


# ------------------------------------------------------------ errors


def test_unknown_route_returns_json_404(client):
    response = client.get("/api/does-not-exist")
    assert response.status_code == 404
    body = response.get_json()
    assert "error" in body


def test_create_many_tasks_and_fetch_all(client):
    for i in range(20):
        _create_task(client, f"Task {i}", f"Description {i}")
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert len(response.get_json()["tasks"]) == 20