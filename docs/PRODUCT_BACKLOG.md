# Product Backlog — Mini-Trello

Priorities: **High** = must have for a usable board; **Medium** = important but not blocking.
Story points use a simple Fibonacci scale (1, 2, 3, 5, 8) commonly used in Scrum.

> Individual project — completed by Jatinsinh Solanki (Enrollment 230390116025).

| ID | User Story                                                                     | Priority | Points | Acceptance Criteria |
| -- | ------------------------------------------------------------------------------ | -------- | ------ | ------------------- |
| US1 | As a user, I want to create a new task so that I can add it to my board.        | High     | 5      | Clicking "Create New Task" opens a form; Title required; Description required; submitting saves the task to the database; the new task appears in the To Do column. |
| US2 | As a user, I want to see all my tasks grouped by status so I know what to work on. | High   | 3      | The page loads three columns (To Do / In Progress / Done); tasks are fetched from the API; every task renders in the column matching its status. |
| US3 | As a user, I want to move a task from To Do to In Progress to Done.             | High     | 5      | Each card has movement controls; clicking a control calls the API; the database status is updated; the UI reflects the new status immediately. |
| US4 | As a user, I want to delete a task if it was created by mistake.                | Medium   | 3      | Each card has a delete control; a confirmation prompt is shown; the database record is deleted; the UI removes the task. |

**Total: 16 story points** for two one-week sprints.

## Point Estimate Justification

- **US1 (5):** touches three layers — validated modal form, new REST endpoint with
  server-side validation, and database insert + immediate UI update.
- **US2 (3):** mostly frontend work — a single GET endpoint plus grouping logic and
  rendering; simple but spans UI structure and loading/empty states.
- **US3 (5):** the most logic-heavy story — movement rules, a partial-update endpoint
  with status validation, and optimistic-but-driven UI updates.
- **US4 (3):** straightforward DELETE endpoint with a 404 path and a confirmation UI;
  low complexity but requires care with state removal.

## Sprint Assignment

| Sprint   | Stories        | Points |
| -------- | -------------- | ------ |
| Sprint 1 | US1, US2 (foundation: DB, GET, POST, board UI) | 8 |
| Sprint 2 | US1 frontend integration, US3, US4            | 8 |