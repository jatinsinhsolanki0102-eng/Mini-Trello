"""
Automated end-to-end assertions for the Mini-Trello UI in a real browser.

Prerequisites: backend on :5000, frontend dev server on :5173,
`python -m playwright install chromium`.

    python scripts/e2e_check.py
"""

import sys
import urllib.request

from playwright.sync_api import sync_playwright

FRONTEND_URL = "http://127.0.0.1:5173"
API_URL = "http://127.0.0.1:5000/api"

PASS = []


def check(name, condition):
    PASS.append((name, bool(condition)))
    print(("PASS" if condition else "FAIL"), "-", name)


def api_delete_all():
    with urllib.request.urlopen(API_URL + "/tasks") as r:
        data = __import__("json").loads(r.read().decode())
    for t in data["tasks"]:
        req = urllib.request.Request(API_URL + f"/tasks/{t['id']}", method="DELETE")
        urllib.request.urlopen(req).close()


def main():
    api_delete_all()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        # Scenario 1: three columns visible
        page.goto(FRONTEND_URL, wait_until="networkidle")
        page.wait_for_selector(".column", timeout=15000)
        titles = page.locator(".column-title").all_inner_texts()
        joined = " ".join(titles).upper()
        check("Three columns visible (To Do/In Progress/Done)", "TO DO" in joined and "IN PROGRESS" in joined and "DONE" in joined)
        check("Loading state replaced by board", not page.locator(".board-loading").count())

        # Scenario 2: modal opens
        page.click("button.btn-create")
        page.wait_for_selector(".modal")
        check("Create New Task modal opens", page.locator(".modal").is_visible())

        # Scenario 3a: whitespace validation
        page.fill("#task-title", "   ")
        page.fill("#task-description", "   ")
        page.click("button[type=submit]")
        check("Frontend rejects whitespace-only title", page.locator(".field-error").count() >= 1)

        # Scenario 3: valid create
        page.fill("#task-title", "Create Database")
        page.fill("#task-description", "Design task database")
        page.click("button[type=submit]")
        page.wait_for_function("() => [...document.querySelectorAll('.task-title')].some(el => el.textContent.includes('Create Database'))", timeout=8000)
        card = page.locator(".column-todo .task-card", has_text="Create Database")
        check("Task appears in To Do column", card.count() == 1)
        check("No Previous button on To Do task", card.locator("button.btn-previous").count() == 0)
        check("Next button shown on To Do task", card.locator("button.btn-next").count() == 1)

        # Scenario 4: move To Do -> In Progress
        card.locator("button.btn-next").click()
        page.wait_for_function("() => [...document.querySelectorAll('.column-in_progress .task-title')].some(el => el.textContent.includes('Create Database'))", timeout=8000)
        move_card = page.locator(".column-in_progress .task-card", has_text="Create Database")
        check("Task moved to In Progress column", move_card.count() == 1)
        check("Previous shown on In Progress", move_card.locator("button.btn-previous").count() == 1)
        check("Next shown on In Progress", move_card.locator("button.btn-next").count() == 1)

        # Scenario 5: move In Progress -> Done
        move_card.locator("button.btn-next").click()
        page.wait_for_function("() => [...document.querySelectorAll('.column-done .task-title')].some(el => el.textContent.includes('Create Database'))", timeout=8000)
        done_card = page.locator(".column-done .task-card", has_text="Create Database")
        check("Task moved to Done column", done_card.count() == 1)
        check("No Next button on Done task", done_card.locator("button.btn-next").count() == 0)
        check("Previous shown on Done", done_card.locator("button.btn-previous").count() == 1)

        # Scenario 6: move back Done -> In Progress
        done_card.locator("button.btn-previous").click()
        page.wait_for_function("() => [...document.querySelectorAll('.column-in_progress .task-title')].some(el => el.textContent.includes('Create Database'))", timeout=8000)
        check("Task moved back to In Progress", page.locator(".column-in_progress .task-card", has_text="Create Database").count() == 1)

        # Scenario 7: delete with confirmation
        db = page.locator(".column-in_progress .task-card", has_text="Create Database")
        db.locator("button.btn-delete").click()
        check("Delete confirmation appears", db.locator(".confirm-box").is_visible())

        db.locator("button.btn-cancel-delete").click()
        check("Cancel keeps task card", db.locator(".task-title", has_text="Create Database").count() == 1)

        db.locator("button.btn-delete").click()
        db.locator("button.btn-confirm-delete").click()
        page.wait_for_function(
            "() => [...document.querySelectorAll('.task-card')].every(el => !el.textContent.includes('Create Database'))",
            timeout=8000,
        )
        check("Task removed from UI after delete", page.locator(".task-card", has_text="Create Database").count() == 0)

        # Empty states
        page.reload(wait_until="networkidle")
        check("Empty state shown in each column", page.locator(".empty-state").count() == 3)

        # Theme: default is dark
        check(
            "Theme defaults to dark",
            page.evaluate("() => document.documentElement.getAttribute('data-theme')") == "dark",
        )

        # Theme: switch to Light
        page.locator(".theme-option", has_text="Light").click()
        page.wait_for_function(
            "() => document.documentElement.getAttribute('data-theme') === 'light'"
        )
        check(
            "Switching to Light updates the document theme",
            page.evaluate("() => document.documentElement.getAttribute('data-theme')") == "light",
        )
        check(
            "Theme preference saved to localStorage",
            page.evaluate("() => localStorage.getItem('mini-trello-theme')") == "light",
        )

        # Theme: persistence across refresh
        page.reload(wait_until="networkidle")
        check(
            "Light theme persists after refresh",
            page.evaluate("() => document.documentElement.getAttribute('data-theme')") == "light",
        )

        # Theme: switch back to Dark
        page.locator(".theme-option", has_text="Dark").click()
        page.wait_for_function(
            "() => document.documentElement.getAttribute('data-theme') === 'dark'"
        )
        check(
            "Switching back to Dark updates the document theme",
            page.evaluate("() => document.documentElement.getAttribute('data-theme')") == "dark",
        )

        browser.close()

    failed = [n for n, ok in PASS if not ok]
    print(f"\n{len(PASS) - len(failed)}/{len(PASS)} checks passed")
    if failed:
        print("Failed:", failed)
        sys.exit(1)


if __name__ == "__main__":
    main()