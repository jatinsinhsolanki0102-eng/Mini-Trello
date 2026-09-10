# Agile Ceremonies — Mini-Trello

This page documents how the Scrum ceremonies were run for this **individual**
project (dates and updates recorded for the record).

---

## 1. Sprint Planning

Held at the start of each sprint. Items were picked from the product backlog
(top priority first) and a sprint goal and a Definition of Done were agreed.

**Sprint 1 goal:** working database + GET/POST APIs + static board UI.
**Sprint 2 goal:** fully functional board where all actions persist.

Planning output: sprint task list in `SPRINT_REPORTS.md`.

## 2. Daily / Regular Progress Updates

A short daily progress check (max 15 minutes), answering:

- What did I complete yesterday?
- What am I working on today?
- Any blockers?

Daily log summary (single contributor — Jatinsinh Solanki):

| Day      | Completed                                     | Working on today             | Blockers |
| -------- | --------------------------------------------- | ---------------------------- | -------- |
| Day 1    | Project setup, requirements                    | Board UI skeleton            | none     |
| Day 1    | —                                             | GET/POST endpoints           | none     |
| Day 1    | —                                             | tasks schema + DB setup      | none     |
| Day 2    | Board sections + header                       | Task card + modal            | none     |
| Day 2    | GET + POST working via HTTP                   | Validation tests             | none     |
| Day 2    | SQLite DB + schema script                     | Seed data                    | none     |
| Day 3    | Full create/move/delete UI integration        | Light/Dark theme + polish    | none     |
| Day 4    | Theme persistence + E2E checks                | Screenshots, report, ZIP     | none     |

## 3. Sprint Review

At the end of each sprint the working increment was demonstrated.

**Sprint 1 review:** showed GET/POST via HTTP, the three-column UI with sample
cards, and the database table.

**Sprint 2 review:** live demo of the full flow — create a task, move it
To Do → In Progress → Done, delete it, refresh the browser to confirm persistence,
plus the Light/Dark theme switcher with localStorage persistence.

## 4. Sprint Retrospective (Sprint 2)

- **What went well:** clear API contract agreed early; the design-token CSS
  approach made theming cheap; end-to-end testing caught bugs before submission.
- **What could improve:** more time for visual polish; start the report earlier.
- **Actions for next time:** design the UI mockup before coding; write tests first
  for new endpoints.