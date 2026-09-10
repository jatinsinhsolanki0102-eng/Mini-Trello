# REST API Reference — Mini-Trello

Base URL: `http://localhost:5000/api` (backend)

All requests and responses use **JSON**. Errors use the shape
`{"error": "<message>"}`.

## Endpoints

| Method | Endpoint          | Purpose                  | Request Body                    | Response                                   | Status |
| ------ | ----------------- | ------------------------ | ------------------------------- | ------------------------------------------ | ------ |
| GET    | `/api/tasks`      | Fetch all tasks          | —                               | `{"tasks": [...]}`                         | 200    |
| POST   | `/api/tasks`      | Create a task            | `{"title": "...", "description": "..."}` | Created task `{"id", "title", "description", "status": "todo", ...}` | 201 |
| PUT    | `/api/tasks/:id`  | Update status/details    | `{"status": "..."}` or `{"title": "...", "description": "..."}` | Updated task object                        | 200    |
| DELETE | `/api/tasks/:id`  | Delete a task            | —                               | `{"message": "Task <id> deleted"}`          | 200    |

### Error statuses

| Status | Example body                             | When                                       |
| ------ | ---------------------------------------- | ------------------------------------------ |
| 400    | `{"error": "Title is required"}`          | blank/missing/invalid field                |
| 400    | `{"error": "Invalid status. Allowed values: todo, in_progress, done"}` | bad status |
| 404    | `{"error": "Task not found"}`             | task id does not exist                     |
| 500    | `{"error": "Internal server error"}`     | unexpected server error                    |

---

## Sample Payloads

### 1. GET /api/tasks → 200 OK

```json
{
  "tasks": [
    {
      "id": 3,
      "title": "Write Project Report",
      "description": "Prepare the final DOCX report with screenshots.",
      "status": "done",
      "created_at": "2026-09-02T05:28:47.783394",
      "updated_at": "2026-09-02T05:29:26.557526"
    }
  ]
}
```

### 2. POST /api/tasks → 201 Created

Request:

```json
{ "title": "Create UI", "description": "Build the Mini-Trello interface" }
```

Response:

```json
{
  "id": 4,
  "title": "Create UI",
  "description": "Build the Mini-Trello interface",
  "status": "todo",
  "created_at": "2026-09-02T06:20:00.000000",
  "updated_at": "2026-09-02T06:20:00.000000"
}
```

### 3. PUT /api/tasks/4 → 200 OK

Request:

```json
{ "status": "in_progress" }
```

Response:

```json
{
  "id": 4,
  "title": "Create UI",
  "description": "Build the Mini-Trello interface",
  "status": "in_progress",
  "created_at": "2026-09-02T06:20:00.000000",
  "updated_at": "2026-09-02T06:21:30.000000"
}
```

### 4. PUT /api/tasks/4 → 200 OK (status → done)

Request:

```json
{ "status": "done" }
```

Response `status` field becomes `"done"`.

### 5. DELETE /api/tasks/4 → 200 OK

Response:

```json
{ "message": "Task 4 deleted" }
```

### 6. Validation error → 400 Bad Request

Request:

```json
{ "title": "", "description": "Something" }
```

Response:

```json
{ "error": "Title is required" }
```

Request:

```json
{ "status": "review" }
```

Response:

```json
{ "error": "Invalid status. Allowed values: todo, in_progress, done" }
```

### 7. Missing task → 404 Not Found

`GET/PUT/DELETE /api/tasks/99999` → `{"error": "Task not found"}`

---

## Status flow enforced by the UI

```
To Do  ──Next──►  In Progress  ──Next──►  Done
   ▲                    │                     │
   └──────Previous──────┘                     └──────Previous──────┘
```

Valid status values persisted in the database: `todo`, `in_progress`, `done`.