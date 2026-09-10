# Sprint Reports — Mini-Trello

The project runs **two one-week sprints**. Dates below are examples — update them
with the real calendar.

---

## Sprint 1 — Foundation & Setup

- **Duration:** 1 week
- **Goal:** Build a solid foundation: a working database, the first two task APIs,
  and a static three-column board.
- **Stories:** US1 (backend part: POST), US2 (GET + board UI)

### Sprint Planning (selected backlog → sprint)

1. Design the `tasks` database schema (id, title, description, status).
2. Create the database (SQLite for dev + `database/schema.sql` for MySQL).
3. Implement the Task model with status validation and DB constraint.
4. Implement `GET /api/tasks`.
5. Implement `POST /api/tasks` (auto status `todo`, validation).
6. Test GET and POST with Postman / curl / pytest.
7. Scaffold the React + Vite frontend.
8. Build the three-column board UI and a first static task card.

### Definition of Done

- `GET /api/tasks` returns 200 + JSON list from the real database.
- `POST /api/tasks` returns 201 with `status = "todo"`; invalid input returns 400.
- A static frontend renders the three columns and sample cards.

### Sprint 1 Report

- Completed: schema, model, GET + POST endpoints, validation, CORS, frontend
  scaffold with Header/Board/Column/TaskCard UI and styles.
- Tested: GET/POST via pytest (green) and live HTTP requests.
- **Deliverable:** working database + GET/POST APIs testable via Postman + static
  frontend UI.

---

## Sprint 2 — Integration & Delivery

- **Duration:** 1 week
- **Goal:** Complete the application: movement and deletion, full frontend–backend
  integration, robustness, and delivery artifacts.
- **Stories:** US1 (frontend integration), US3, US4

### Sprint Retrospective (Sprint 1, 15 min)

- Went well: schema and API contract were agreed first, which made integration smooth.
- Learning: the modal UX needed more thought than expected — kept it minimal.
- Action: spend Sprint 2 on the update/delete endpoints early to unblock the UI.

### Sprint Planning (selected backlog → sprint)

1. Implement `PUT /api/tasks/<id>` (update status/title/description, validation, 404).
2. Implement `DELETE /api/tasks/<id>` (validation, 404).
3. Connect frontend to backend via a centralized API service (`services/api.js`).
4. Implement task creation in the UI (modal + validation + POST).
5. Implement task movement (Next / Previous buttons calling PUT).
6. Implement delete with inline confirmation.
7. Add loading and error states; handle all request failures gracefully.
8. Iterate on responsive design and polish.
9. Test the complete application (pytest + live end-to-end).
10. Fix bugs found in end-to-end testing.
11. Capture screenshots (`scripts/capture_screenshots.py`).
12. Write README, project report, and prepare the source ZIP.

### Sprint 2 Report

- Completed: all required APIs, full frontend–backend integration, movement +
  delete flows, validation on both sides, responsive UI, 26 pytest cases passing,
  real-browser verification, screenshots, README, report.
- Fixes found in E2E testing: replaced blocking `window.confirm` with an inline
  confirmation UI; corrected an API demo path in the screenshot script.
- **Deliverable:** fully functional Mini-Trello where every frontend action
  persists in the database.

---

## Sprint Burndown (example — update with real data)

| Day | Sprint 1 open tasks | Sprint 2 open tasks |
| --- | ------------------- | ------------------- |
| Mon | 8 | 11 |
| Tue | 6 | 9 |
| Wed | 5 | 6 |
| Thu | 2 | 3 |
| Fri | 0 | 0 |