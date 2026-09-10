"""Backend API tests for Mini-Trello (authenticated, per-user boards)."""

VALID_TITLE = "Design Database"
VALID_DESCRIPTION = "Create MySQL schema for tasks"


def _create_task(client, auth, title=VALID_TITLE, description=VALID_DESCRIPTION):
    return client.post(
        "/api/tasks",
        json={"title": title, "description": description},
        headers=auth,
    )


# ------------------------------------------------------------ auth


def test_register_returns_token_and_user(client):
    response = client.post(
        "/api/auth/register",
        json={"username": "bob", "password": "secret123"},
    )
    assert response.status_code == 201
    body = response.get_json()
    assert "token" in body
    assert body["user"]["username"] == "bob"
    assert "id" in body["user"]


def test_register_requires_minimum_password(client):
    response = client.post(
        "/api/auth/register",
        json={"username": "bob", "password": "12345"},
    )
    assert response.status_code == 400
    assert "Password" in response.get_json()["error"]


def test_register_rejects_duplicate_username(client):
    first = client.post(
        "/api/auth/register",
        json={"username": "alice", "password": "secret123"},
    )
    assert first.status_code == 201
    second = client.post(
        "/api/auth/register",
        json={"username": "alice", "password": "other123"},
    )
    assert second.status_code == 409


def test_login_with_valid_credentials(client):
    client.post(
        "/api/auth/register",
        json={"username": "alice", "password": "secret123"},
    )
    response = client.post(
        "/api/auth/login",
        json={"username": "alice", "password": "secret123"},
    )
    assert response.status_code == 200
    assert "token" in response.get_json()


def test_login_with_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={"username": "alice", "password": "secret123"},
    )
    response = client.post(
        "/api/auth/login",
        json={"username": "alice", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_me_returns_current_user(client, auth, token):
    response = client.get("/api/auth/me", headers=auth)
    assert response.status_code == 200
    assert response.get_json()["user"]["username"] == "alice"


def test_task_requests_require_auth(client):
    assert client.get("/api/tasks").status_code == 401
    assert (
        client.post("/api/tasks", json={"title": "X", "description": "Y"}).status_code
        == 401
    )
    assert client.put("/api/tasks/1", json={"status": "done"}).status_code == 401
    assert client.delete("/api/tasks/1").status_code == 401


def test_invalid_token_is_rejected(client):
    response = client.get("/api/tasks", headers={"Authorization": "Bearer nonsense"})
    assert response.status_code == 401


# ----------------------------------------------------------- GET tasks


def test_get_empty_database_returns_empty_list(client, auth):
    response = client.get("/api/tasks", headers=auth)
    assert response.status_code == 200
    assert response.get_json() == {"tasks": []}


def test_get_tasks_returns_all_created_tasks(client, auth):
    _create_task(client, auth, "Task A", "Description A")
    _create_task(client, auth, "Task B", "Description B")

    response = client.get("/api/tasks", headers=auth)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["tasks"]) == 2
    titles = {task["title"] for task in data["tasks"]}
    assert titles == {"Task A", "Task B"}


def test_boards_are_private_between_users(client, auth):
    """Tasks made by one user must not be visible to another user."""
    _create_task(client, auth, "Alice's secret task", "private")

    other = client.post(
        "/api/auth/register",
        json={"username": "eve", "password": "secret123"},
    ).get_json()
    other_auth = {"Authorization": f"Bearer {other['token']}"}

    seen = client.get("/api/tasks", headers=other_auth).get_json()["tasks"]
    assert seen == []


def test_cannot_modify_another_users_task(client, auth, token):
    created = _create_task(client, auth, "Alice's task", "private").get_json()

    other = client.post(
        "/api/auth/register",
        json={"username": "eve", "password": "secret123"},
    ).get_json()
    other_auth = {"Authorization": f"Bearer {other['token']}"}

    put = client.put(
        f"/api/tasks/{created['id']}", json={"status": "done"}, headers=other_auth
    )
    assert put.status_code == 404
    delete = client.delete(f"/api/tasks/{created['id']}", headers=other_auth)
    assert delete.status_code == 404


# ---------------------------------------------------------- POST task


def test_create_task_returns_201_with_todo_status(client, auth):
    response = _create_task(client, auth)
    assert response.status_code == 201
    body = response.get_json()
    assert body["title"] == VALID_TITLE
    assert body["description"] == VALID_DESCRIPTION
    assert body["status"] == "todo"
    assert isinstance(body["id"], int)


def test_create_task_persists_in_database(client, auth):
    created = _create_task(client, auth).get_json()
    response = client.get("/api/tasks", headers=auth)
    assert len(response.get_json()["tasks"]) == 1
    assert response.get_json()["tasks"][0]["id"] == created["id"]


def test_create_task_trims_whitespace(client, auth):
    response = client.post(
        "/api/tasks",
        json={
            "title": "   Trimmed title   ",
            "description": "   Trimmed description   ",
        },
        headers=auth,
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body["title"] == "Trimmed title"
    assert body["description"] == "Trimmed description"


# --------------------------------------------------- POST validation


def test_post_empty_title_returns_400(client, auth):
    response = client.post(
        "/api/tasks",
        json={"title": "", "description": "Something"},
        headers=auth,
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_post_missing_title_returns_400(client, auth):
    response = client.post(
        "/api/tasks", json={"description": "Something"}, headers=auth
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_post_whitespace_only_title_returns_400(client, auth):
    response = client.post(
        "/api/tasks", json={"title": "   ", "description": "Something"}, headers=auth
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_post_empty_description_returns_400(client, auth):
    response = client.post(
        "/api/tasks", json={"title": "Create UI", "description": ""}, headers=auth
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Description is required"


def test_post_missing_description_returns_400(client, auth):
    response = client.post("/api/tasks", json={"title": "Create UI"}, headers=auth)
    assert response.status_code == 400
    assert response.get_json()["error"] == "Description is required"


def test_post_non_json_body_returns_400(client, auth):
    response = client.post(
        "/api/tasks", data="not json", content_type="text/plain", headers=auth
    )
    assert response.status_code == 400


def test_post_does_not_accept_arbitrary_status(client, auth):
    response = client.post(
        "/api/tasks",
        json={"title": "X", "description": "Y", "status": "done"},
        headers=auth,
    )
    assert response.status_code == 201
    # A new task always starts in "todo", the provided status is ignored.
    assert response.get_json()["status"] == "todo"


# ---------------------------------------------------------- PUT task


def test_update_status_to_in_progress(client, auth):
    task_id = _create_task(client, auth).get_json()["id"]
    response = client.put(
        f"/api/tasks/{task_id}", json={"status": "in_progress"}, headers=auth
    )
    assert response.status_code == 200
    assert response.get_json()["status"] == "in_progress"


def test_update_status_to_done(client, auth):
    task_id = _create_task(client, auth).get_json()["id"]
    response = client.put(
        f"/api/tasks/{task_id}", json={"status": "done"}, headers=auth
    )
    assert response.status_code == 200
    assert response.get_json()["status"] == "done"


def test_full_status_transition_sequence(client, auth):
    task_id = _create_task(client, auth).get_json()["id"]

    r1 = client.put(
        f"/api/tasks/{task_id}", json={"status": "in_progress"}, headers=auth
    )
    assert r1.get_json()["status"] == "in_progress"

    r2 = client.put(f"/api/tasks/{task_id}", json={"status": "done"}, headers=auth)
    assert r2.get_json()["status"] == "done"

    r3 = client.put(f"/api/tasks/{task_id}", json={"status": "todo"}, headers=auth)
    assert r3.get_json()["status"] == "todo"


def test_update_title_and_description(client, auth):
    task_id = _create_task(client, auth).get_json()["id"]
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "New title", "description": "New description"},
        headers=auth,
    )
    body = response.get_json()
    assert response.status_code == 200
    assert body["title"] == "New title"
    assert body["description"] == "New description"


# --------------------------------------------------- PUT validation


def test_update_invalid_status_returns_400(client, auth):
    task_id = _create_task(client, auth).get_json()["id"]
    response = client.put(
        f"/api/tasks/{task_id}", json={"status": "review"}, headers=auth
    )
    assert response.status_code == 400
    assert "Invalid status" in response.get_json()["error"]


def test_update_nonexistent_task_returns_404(client, auth):
    response = client.put(
        "/api/tasks/99999", json={"status": "done"}, headers=auth
    )
    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found"


def test_update_with_empty_title_returns_400(client, auth):
    task_id = _create_task(client, auth).get_json()["id"]
    response = client.put(
        f"/api/tasks/{task_id}", json={"title": "  "}, headers=auth
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_update_with_empty_body_returns_400(client, auth):
    task_id = _create_task(client, auth).get_json()["id"]
    response = client.put(f"/api/tasks/{task_id}", json={}, headers=auth)
    assert response.status_code == 400


# -------------------------------------------------------- DELETE task


def test_delete_task_removes_it(client, auth):
    task_id = _create_task(client, auth).get_json()["id"]
    response = client.delete(f"/api/tasks/{task_id}", headers=auth)
    assert response.status_code == 200
    assert response.get_json()["message"] == f"Task {task_id} deleted"

    remaining = client.get("/api/tasks", headers=auth).get_json()["tasks"]
    assert remaining == []


def test_delete_nonexistent_task_returns_404(client, auth):
    response = client.delete("/api/tasks/99999", headers=auth)
    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found"


def test_delete_does_not_affect_other_tasks(client, auth):
    _create_task(client, auth, "Keep me", "description")
    doomed = _create_task(client, auth, "Delete me", "description").get_json()["id"]

    client.delete(f"/api/tasks/{doomed}", headers=auth)

    remaining = client.get("/api/tasks", headers=auth).get_json()["tasks"]
    assert len(remaining) == 1
    assert remaining[0]["title"] == "Keep me"


# ------------------------------------------- columns grouping support


def test_get_returns_tasks_with_all_statuses_for_columns(client, auth):
    t1 = _create_task(client, auth, "To do task", "d").get_json()
    t2 = _create_task(client, auth, "Wip task", "d").get_json()
    t3 = _create_task(client, auth, "Done task", "d").get_json()

    client.put(f"/api/tasks/{t2['id']}", json={"status": "in_progress"}, headers=auth)
    client.put(f"/api/tasks/{t3['id']}", json={"status": "done"}, headers=auth)

    tasks = client.get("/api/tasks", headers=auth).get_json()["tasks"]
    by_status = {task["id"]: task["status"] for task in tasks}
    assert by_status[t1["id"]] == "todo"
    assert by_status[t2["id"]] == "in_progress"
    assert by_status[t3["id"]] == "done"


# ------------------------------------------------------------ errors


def test_unknown_route_returns_json_404(client, auth):
    response = client.get("/api/does-not-exist", headers=auth)
    assert response.status_code == 404
    body = response.get_json()
    assert "error" in body


def test_create_many_tasks_and_fetch_all(client, auth):
    for i in range(20):
        _create_task(client, auth, f"Task {i}", f"Description {i}")
    response = client.get("/api/tasks", headers=auth)
    assert response.status_code == 200
    assert len(response.get_json()["tasks"]) == 20