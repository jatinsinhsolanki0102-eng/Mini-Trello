# Mini-Trello — Report Content

This file contains the full written content of the project report. `scripts/generate_report.py`
turns it into a ready-to-submit **DOCX** (including real screenshots and tables).

---

## Cover / Student Details

| Field            | Value                        |
| ---------------- | ---------------------------- |
| Project          | Mini-Trello Kanban Board     |
| Student Name     | Jatinsinh Solanki            |
| Enrollment Number| 230390116025                 |
| Team             | Individual                   |
| Semester         | 7th Semester                 |
| Subject          | Software Engineering (Agile/Scrum) |

## Project Overview

Mini-Trello is a simple, modern, responsive single-page Kanban task-management
application. It lets a user create tasks, view them grouped into three status
columns (To Do, In Progress, Done), move tasks between columns, and delete tasks.
All data is stored in a real database and every action is performed through a
RESTful API, so the board state survives browser refreshes.

The project was developed to practice the full stack — frontend UI in React,
backend REST API in Flask, and a relational database (MySQL; SQLite used locally
for zero-setup development) — while applying the Agile/Scrum methodology over two
one-week sprints.

**How Kanban works:** work is visualized as cards flowing through columns that
represent stages. Limiting work-in-progress and moving cards only in the allowed
direction keeps the team focused and the workflow visible.

## Objectives

- Build a task-management board with three columns and full create/move/delete.
- Implement a RESTful API (GET, POST, PUT, DELETE) with JSON in/out.
- Store tasks in a real database with persistence across restarts.
- Integrate a React frontend with a Flask backend over HTTP.
- Apply Agile/Scrum with two one-week sprints and all ceremonies.

## Technology Stack

| Layer      | Technology                         |
| ---------- | ---------------------------------- |
| Frontend   | React 19, JavaScript (ES modules), CSS custom properties (design tokens), Vite 6 |
| Backend    | Python 3.13, Flask 3.1, Flask-CORS, SQLAlchemy 2 |
| Database   | MySQL 8 (schema provided); SQLite as zero-setup local default |
| UI / Theming | Dark purple signature theme + Light theme, persisted in localStorage |
| API        | REST, JSON                        |
| Testing    | Pytest (26 cases), Playwright (browser E2E + screenshots) |

## System Architecture

```
Browser (React SPA, Vite)  http://localhost:5173
        │  fetch()
        ▼
REST API  http://localhost:5173/api/*  (Vite dev proxy → Flask :5000)
        │
        ▼
Flask backend  (CORS, routes, validation, error handlers)
        │  SQLAlchemy ORM (parameterized queries)
        ▼
Database  (tasks table — SQLite / MySQL)
```

## Database Design

The application uses a single `tasks` table:

| Column        | Type              | Notes                             |
| ------------- | ----------------- | --------------------------------- |
| `id`          | INT (PK, auto-inc) | unique task id                    |
| `title`       | VARCHAR(200)      | required                          |
| `description` | TEXT              | required                          |
| `status`      | VARCHAR(20)       | `todo` / `in_progress` / `done` (DB CHECK constraint) |
| `created_at`  | DATETIME          | set automatically                 |
| `updated_at`  | DATETIME          | updated on change                 |

The schema script for MySQL lives in `database/schema.sql`.

## User Stories

| ID | As a user... | I want to... | Priority | Points |
| -- | ------------ | ------------ | -------- | ------ |
| US1 | — | create a new task so that I can add it to my board | High | 5 |
| US2 | — | see all my tasks grouped by status so I know what to work on | High | 3 |
| US3 | — | move a task from To Do to In Progress to Done | High | 5 |
| US4 | — | delete a task if it was created by mistake | Medium | 3 |

Full acceptance criteria in `docs/PRODUCT_BACKLOG.md`.

## Product Backlog Summary

- US1 (5pts), US2 (3pts), US3 (5pts), US4 (3pts) — total **16 points**.
- Sprint 1: US1 + US2 (foundation). Sprint 2: US3 + US4 + integration.

## Sprint 1 — Foundation & Setup

- **Goal:** working database, GET/POST endpooints, static board UI.
- Completed: schema, Task model, `GET /api/tasks`, `POST /api/tasks`, validation,
  CORS, React scaffold with the three-column board UI.
- Tested via pytest and live HTTP; deliverable: DB + GET/POST APIs + static UI.

## Sprint 2 — Integration & Delivery

- **Goal:** complete integration and delivery.
- Completed: `PUT /api/tasks/:id`, `DELETE /api/tasks/:id`, frontend connected via
  a centralized API service, create/move/delete in the UI, inline delete
  confirmation, loading + error states, responsive polish, final purple UI
  redesign with **Light/Dark themes** persisted in localStorage, 26 pytest cases,
  23 browser E2E checks (including theme switching), screenshots in both themes,
  README + report + ZIP.

## UI Design & Theming

The final UI is a modern purple-based design system. All colours and shadows are
defined once as CSS custom properties (design tokens) in
`frontend/src/styles/styles.css`, so theme switching never causes layout shifts.

- **Dark Mode (default / signature):** purple-black background (`#0F0B1A`), raised
  purple surfaces, high-contrast text, purple (`#7C3AED`) accent buttons.
- **Light Mode:** soft lavender background (`#F7F5FC`) with white cards, the same
  purple accents, and identical layout.
- Segmented **Light | Dark** selector in the header; saved under
  `mini-trello-theme` in `localStorage`, restored before first paint (no flash).
- Colour-coded status accents per column (purple To Do / violet In Progress /
  green Done) with matching badges on cards; rounded icon buttons, soft shadows,
  subtle animation that respects `prefers-reduced-motion`; responsive
  breakpoints at 960 / 640 / 420 px.

Theme behaviour is covered by automated checks: default dark, switch to light,
persistence after refresh, switch back to dark.

## REST API

See `docs/API_TABLE.md` for the full reference. Summary:

| Method | Endpoint          | Purpose             | Status |
| ------ | ----------------- | ------------------- | ------ |
| GET    | `/api/tasks`      | fetch all tasks     | 200    |
| POST   | `/api/tasks`      | create task (`todo`)| 201    |
| PUT    | `/api/tasks/:id`  | update status/fields| 200    |
| DELETE | `/api/tasks/:id`  | delete task         | 200    |

Errors: 400 (validation), 404 (missing task), 500 (server).

Sample request:

```json
{ "title": "Create UI", "description": "Build the Mini-Trello interface" }
```

Sample response (201):

```json
{ "id": 1, "title": "Create UI", "description": "Build the Mini-Trello interface", "status": "todo" }
```

## Testing

### Unit / integration tests (pytest) — all passed

| # | Test case                            | Input / action                    | Expected result               | Actual result | Status |
| - | ------------------------------------ | --------------------------------- | ----------------------------- | ------------- | ------ |
| 1 | GET empty DB                         | `GET /api/tasks`                  | 200 `{"tasks": []}`           | 200 `[]`      | Pass   |
| 2 | GET multiple tasks                   | create 2, then GET                | 200, both tasks returned      | 200, both     | Pass   |
| 3 | POST task                            | valid title+description           | 201, status `todo`            | 201 `todo`    | Pass   |
| 4 | POST empty title                     | `title=""`                        | 400 "Title is required"       | 400           | Pass   |
| 5 | POST empty description               | `description=""`                  | 400 "Description is required" | 400           | Pass   |
| 6 | PUT status                           | `{"status":"in_progress"}`        | 200, status updated           | 200           | Pass   |
| 7 | PUT invalid status                   | `{"status":"review"}`             | 400 invalid status            | 400           | Pass   |
| 8 | PUT nonexistent task                 | `PUT /api/tasks/99999`            | 404 "Task not found"          | 404           | Pass   |
| 9 | DELETE task                         | `DELETE /api/tasks/:id`           | 200 + task removed            | 200, removed   | Pass   |
| 10 | DELETE nonexistent task             | `DELETE /api/tasks/99999`         | 404                            | 404           | Pass   |
| 11 | Full status transitions             | todo→in_progress→done→todo        | all transitions persist       | all pass      | Pass   |
| 12 | Trimming whitespace                 | title/desc with spaces            | stored trimmed                | trimmed       | Pass   |
| 13 | Columns grouping                    | 3 tasks each status               | GET returns matching statuses | correct       | Pass   |
| 14 | Write-only GET isolation            | transient check                   | unaffected                    | unaffected    | Pass   |

Command: `python -m pytest -q` → **26 passed**.

### End-to-end / browser verification

- Live API: create → move → delete → refresh (all verified, see screenshots).
- Persistence test: task created and moved, then the server was fully restarted —
  data and new status were still present on reload.
- Real browser flows exercised with Playwright (create modal, movement buttons,
  inline delete confirmation, mobile layout) — **23/23 checks passed**, including:
  - Theme defaults to **dark**.
  - Switching to **Light** updates the document theme and `localStorage`.
  - Light theme **persists after a refresh** (picked up before first paint).
  - Switching back to **Dark** works and is the final state.

### Frontend validation

- Modal rejects empty/whitespace-only Title and Description with inline messages.
- Errors from the server are displayed in a banner; the board never crashes.

## Screenshots

Real screenshots captured from the running application (`screenshots/` folder;
light and dark themes — dark is the signature theme):

1. `01-board-light.png` — main board (Light theme, three columns with tasks)
2. `02-board-dark.png` — main board (Dark theme)
3. `03-modal-light.png` — Create Task modal filled (Light)
4. `04-modal-dark.png` — Create Task modal filled (Dark)
5. `05-task-in-todo.png` — task in To Do
6. `06-task-in-progress.png` — task moved to In Progress
7. `07-task-in-done.png` — task moved to Done
8. `08-delete-confirmation.png` — inline delete confirmation
9. `09-database-table.png` — tasks table with live data
10. `10-mobile-dark.png` — responsive mobile layout (Dark)
11. `11-api-testing.png` — live REST requests/responses (Postman-equivalent)

## Agile Execution Summary

Two one-week sprints with planning, daily stand-ups, review, and retrospective
(details in `docs/`). Product backlog of 4 user stories, 16 story points.
Responsibility table in `docs/RESPONSIBILITIES.md`. Ceremonies in
`docs/AGILE_CEREMONIES.md`.

## Future Improvements

- Drag-and-drop between columns; in-place card editing
- Optional `assigned_to` field and assignee filters
- Search/filter/pagination; notifications
- Deployment (frontend on Vercel/Netlify, backend on Render/Railway)