# Mini-Trello

A simple, modern, responsive **single-page Kanban task management board** built as a
7th-semester college project. Tasks are stored in a real database and all changes are
made through a REST API.

- **Board:** three columns — To Do, In Progress, Done
- **Actions:** create tasks, move tasks (Next / Previous), delete tasks (with confirmation)
- **Persistence:** every action is written to the database; refreshing the browser keeps state

---

## Features

- Single-page Kanban board with three columns: **To Do**, **In Progress**, **Done**
- Create new tasks via a validated modal form
- Move tasks forward (`To Do → In Progress → Done`) and backward (`Done → In Progress → To Do`)
- **Drag and drop** tasks between columns (HTML5 DnD, works on desktop browsers)
- Animated card transitions — cards fly out smoothly and drop into the next column
- **Live animated background** — a slowly flowing colour gradient in both themes
- Delete tasks with an inline confirmation
- Task cards show title, description, and a coloured status badge
- **Light Mode and Dark Mode** (dark purple is the signature theme), user-selectable
  and persisted in `localStorage`
- Loading state, empty states, and friendly error banners
- Fully responsive (desktop, tablet, mobile)
- REST API with JSON validation and proper error handling
- Backend automated tests (26 pytest cases) + browser end-to-end checks (23)

## Theme Support

Mini-Trello ships a modern **purple-based design system** with two full themes.

- **Dark Mode (default)** — dark purple-black background with purple surfaces,
  high-contrast light text, and purple accent buttons.
- **Light Mode** — very light purple/white background with white cards and purple accents.

The header contains a **segmented theme selector** (`☀ Light | ☾ Dark`). The choice is
applied instantly across the whole app (CSS custom-property design tokens, no layout
shifts) and saved to `localStorage` under the key **`mini-trello-theme`**, so it
survives page refreshes. On load, a small inline script applies the saved theme before
the first paint to avoid any flash of the wrong theme.

All colours are defined as design tokens (CSS variables under `:root` and
`:root[data-theme="light"]`) in `frontend/src/styles/styles.css` — nothing is hardcoded
in components. Animations are short and respect `prefers-reduced-motion`.

## Tech Stack

| Layer      | Technology                         |
| ---------- | ---------------------------------- |
| Frontend   | React, JavaScript, CSS, Vite       |
| Backend    | Python, Flask, Flask-CORS, SQLAlchemy |
| Database   | MySQL (default in SQLite for zero-setup local dev) |
| API        | RESTful, JSON                      |
| Testing    | Pytest (backend)                   |

> **Database note.** The project was developed with a database abstraction layer
> (SQLAlchemy). Locally it runs on **SQLite** out of the box so the project works
> immediately with no server installation. To use **MySQL** (as required), create the
> database once with `database/schema.sql` and set `DATABASE_URL` in
> `backend/.env` (see below). No code changes are needed.

## Architecture

```
Browser (React SPA)
    │  fetch()  →  http://localhost:5173/api/*   (Vite proxy → Flask)
    ▼
Flask REST API  (backend, port 5000)
    │  SQLAlchemy
    ▼
Database (SQLite / MySQL)
```

## Folder Structure

```
Mini-Trello/
├── frontend/                 # React + Vite single-page application
│   ├── src/
│   │   ├── components/       # Header, Board, Column, TaskCard, TaskModal
│   │   ├── services/api.js   # centralized REST client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles/styles.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── backend/                  # Flask REST API
│   ├── app/
│   │   ├── routes/tasks.py   # GET/POST/PUT/DELETE tasks
│   │   ├── models.py         # Task model + status constants
│   │   ├── config.py         # env-based configuration
│   │   └── __init__.py       # app factory, CORS, error handlers
│   ├── tests/test_tasks.py   # 26 pytest cases
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
├── database/schema.sql       # MySQL creation script
├── scripts/capture_screenshots.py  # captures REPORT screenshots (Playwright)
├── docs/                     # Agile docs, report content, API table
├── screenshots/              # captured screenshots for the report
├── .gitignore
└── README.md
```

## Quick Start (Windows - Recommended)

**Prerequisites:** [Python 3.9+](https://www.python.org/downloads/) and [Node.js 18+](https://nodejs.org/).
When installing Python, **check the box "Add Python to PATH"**.

### Option A: One-Click Launch (Easiest)

1. **First time only** — double-click **`INSTALL.bat`** (installs all dependencies)
2. **Every time** — double-click **`START.bat`** (starts both servers)
3. Wait ~10 seconds, then your browser opens automatically to **http://localhost:5173**

> To stop the project, close both black terminal windows that opened.

### Option B: Manual Launch (Two Terminals)

Open **two separate terminal/command prompt windows**:

**Terminal 1 — Backend (Flask API):**
```bash
cd backend
pip install -r requirements.txt
python run.py
```

**Terminal 2 — Frontend (React + Vite):**
```bash
cd frontend
npm install
npm run dev
```

Then open **http://localhost:5173** in your browser.

> **Important:** Both servers MUST be running at the same time. The frontend
> on port 5173 sends API requests to the backend on port 5000. If the backend
> is not running, you will see errors and tasks will not load.

### 3. MySQL (optional, instead of SQLite)

1. Run the schema script:

   ```bash
   mysql -u root -p < database/schema.sql
   ```

2. Create `backend/.env`:

   ```env
   DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/mini_trello
   ```

3. Restart the backend. The tables are created automatically on startup.

### Production build (frontend)

```bash
cd frontend
npm run build      # outputs to dist/
npm run preview
```

When serving the built app separately, set `VITE_API_URL` to the backend URL
in `frontend/.env` and rebuild.

## Environment Variables

### `backend/.env` (copy from `backend/.env.example`)

| Variable        | Default                          | Purpose                          |
| --------------- | -------------------------------- | -------------------------------- |
| `DATABASE_URL`  | `sqlite:///mini_trello.db`       | Database connection string       |
| `PORT`          | `5000`                           | Flask server port                |
| `CORS_ORIGINS`  | localhost/127.0.0.1:5173,5174    | Allowed frontend origins         |

### `frontend/.env` (optional, copy from `frontend/.env.example`)

| Variable         | Default | Purpose                             |
| ---------------- | ------- | ----------------------------------- |
| `VITE_API_URL`   | `/api`  | Backend base URL (used outside Vite proxy) |

> Secrets live only in `.env`, which is excluded from Git by `.gitignore`. Real
> passwords are never committed.

## REST API

Base URL: `http://localhost:5000/api`

| Method | Endpoint           | Purpose                    | Request Body                    | Response                       | Status            |
| ------ | ------------------ | -------------------------- | ------------------------------- | ------------------------------ | ----------------- |
| GET    | `/tasks`           | List all tasks             | —                               | `{"tasks": [... ]}`            | 200 OK            |
| POST   | `/tasks`           | Create a task (status=todo)| `{"title","description"}`       | created task object            | 201 Created       |
| PUT    | `/tasks/:id`       | Update status/details      | `{"status"}` / `{"title",...}`  | updated task object            | 200 OK            |
| DELETE | `/tasks/:id`       | Delete a task              | —                               | `{"message": "Task N deleted"}`| 200 OK            |

Errors are returned as `{"error": "<message>"}` with status 400 / 404 / 500.

### Sample request / response

**POST** `http://localhost:5000/api/tasks`

```json
{ "title": "Create UI", "description": "Build the Mini-Trello interface" }
```

```json
{ "id": 1, "title": "Create UI", "description": "Build the Mini-Trello interface", "status": "todo" }
```

**PUT** `http://localhost:5000/api/tasks/1`

```json
{ "status": "in_progress" }
```

```json
{ "id": 1, "title": "Create UI", "description": "Build the Mini-Trello interface", "status": "in_progress" }
```

### Validation rules

- `title` — required, must not be blank after trimming
- `description` — required, must not be blank after trimming
- `status` — must be one of `todo`, `in_progress`, `done` (also enforced by a DB constraint)
- New tasks always start with `status = "todo"`

## Database Schema

`tasks` table:

| Column        | Type              | Notes                                  |
| ------------- | ----------------- | -------------------------------------- |
| `id`          | INT (PK, AI)      | auto-increment primary key             |
| `title`       | VARCHAR(200)      | required                               |
| `description` | TEXT              | required                               |
| `status`      | VARCHAR(20)       | `todo` / `in_progress` / `done`        |
| `created_at`  | DATETIME          | set automatically                      |
| `updated_at`  | DATETIME          | updated on change                      |

## Testing

### Backend unit tests

```bash
cd backend
python -m pytest -q
```

Covers: GET (empty + populated), POST (valid, empty/missing/whitespace title,
empty/missing description, non-JSON), PUT status/title/description, invalid status,
404 for missing tasks, DELETE (success, 404, isolation), status transitions, and
multi-task retrieval. **Result: 26 passed.**

### End-to-end (manual / automated)

- Live API verified against the running server (create → move → delete → refresh).
- Browser E2E assertions (`scripts/e2e_check.py`, Playwright): run with backend on
  `:5000` and frontend dev server on `:5173`, then `python scripts/e2e_check.py`.
  Covers the full board flow plus **theme switching and persistence**
  (default dark → switch light → localStorage → survives refresh → switch dark).
  **Result: 23/23 checks passed.**
- Real browser flow screenshots captured with Playwright in both themes
  (see `scripts/capture_screenshots.py`, screenshots in `screenshots/`).
- Persistence proven: tasks and status changes survive a full server restart.

## Agile / Scrum

The project follows two one-week sprints. Full documentation is in `docs/`:

- `docs/PRODUCT_BACKLOG.md` — user stories, priorities, story points, acceptance criteria
- `docs/SPRINT_REPORTS.md` — Sprint 1 & Sprint 2 plans, tasks, deliverables
- `docs/AGILE_CEREMONIES.md` — planning, daily updates, review, retrospective
- `docs/RESPONSIBILITIES.md` — role responsibilities (individual project)
- `docs/API_TABLE.md` — API reference with sample payloads

## Screenshots

Real screenshots captured from the running application are in `screenshots/`
(light and dark themes — dark is the signature theme):

`01-board-light.png` (board, light) · `02-board-dark.png` (board, dark) ·
`03-modal-light.png` (create modal, light) · `04-modal-dark.png` (create modal, dark) ·
`05-task-in-todo.png` · `06-task-in-progress.png` · `07-task-in-done.png` ·
`08-delete-confirmation.png` · `09-database-table.png` · `10-mobile-dark.png` ·
`11-api-testing.png`

## Future Improvements

- Drag and drop between columns (HTML5 DnD)
- Edit task title/description in place
- Optional `assigned_to` field (not required by the assignment)
- Pagination / search / filters
- Deploy the app (e.g., Render/Railway for backend, Vercel/Netlify for frontend)