"""
Capture real screenshots of the redesigned Mini-Trello application
(light + dark themes) for the project report.

Prerequisites (run first):
    npm install && npm run dev   (frontend on http://127.0.0.1:5173)
    python run.py                (backend on http://127.0.0.1:5000)
    python -m playwright install chromium

Usage:
    python scripts/capture_screenshots.py
"""

import json
import time
import urllib.request

from playwright.sync_api import sync_playwright

FRONTEND_URL = "http://127.0.0.1:5173"
API_URL = "http://127.0.0.1:5000/api"
SCREENSHOT_DIR = "screenshots"

SEED_TASKS = [
    {"title": "Design Database Schema", "description": "Create the MySQL schema for the tasks table.", "status": "todo"},
    {"title": "Build REST API", "description": "Implement GET and POST /api/tasks endpoints in Flask.", "status": "in_progress"},
    {"title": "Write Project Report", "description": "Prepare the final DOCX report with screenshots.", "status": "done"},
]


def http(method, path, body=None):
    url = API_URL + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode())


def reset_database():
    _, tasks = http("GET", "/tasks")
    for task in tasks["tasks"]:
        http("DELETE", f"/tasks/{task['id']}")

    for seed in SEED_TASKS:
        _, created = http(
            "POST", "/tasks", {"title": seed["title"], "description": seed["description"]}
        )
        if seed["status"] != "todo":
            http("PUT", f"/tasks/{created['id']}", {"status": seed["status"]})
    print("Database reset with demo data.")


def shot(page, name):
    page.screenshot(path=f"{SCREENSHOT_DIR}/{name}")
    print("Saved", name)


def set_theme(page, theme):
    target = "Light" if theme == "light" else "Dark"
    page.locator(".theme-option", has_text=target).click()
    page.wait_for_function(
        f"() => document.documentElement.getAttribute('data-theme') === '{theme}'"
    )
    time.sleep(0.35)


def capture_ui_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(FRONTEND_URL, wait_until="networkidle")
        page.wait_for_selector(".task-card", timeout=15000)

        # ----- light mode board
        set_theme(page, "light")
        time.sleep(0.4)
        shot(page, "01-board-light.png")

        # ----- dark mode board (signature theme)
        set_theme(page, "dark")
        time.sleep(0.4)
        shot(page, "02-board-dark.png")

        # ----- create modal in light mode (filled)
        set_theme(page, "light")
        page.click("button.btn-create")
        page.wait_for_selector(".modal", timeout=5000)
        page.fill("#task-title", "Watch Tutorials")
        page.fill("#task-description", "Watch the Flask + React tutorial before writing code.")
        time.sleep(0.35)
        shot(page, "03-modal-light.png")
        page.click("button[type=submit]")
        page.wait_for_function(
            "() => [...document.querySelectorAll('.task-title')].some(el => el.textContent.includes('Watch Tutorials'))",
            timeout=8000,
        )

        # ----- create modal in dark mode (empty, then filled)
        set_theme(page, "dark")
        page.click("button.btn-create")
        page.wait_for_selector(".modal", timeout=5000)
        page.fill("#task-title", "Refactor API Service")
        page.fill("#task-description", "Keep all HTTP calls in services/api.js.")
        time.sleep(0.35)
        shot(page, "04-modal-dark.png")
        page.click("button[type=submit]")
        page.wait_for_function(
            "() => [...document.querySelectorAll('.task-title')].some(el => el.textContent.includes('Refactor API Service'))",
            timeout=8000,
        )

        # ----- dark flow: task in To Do
        time.sleep(0.4)
        shot(page, "05-task-in-todo.png")

        # ----- move to In Progress
        todo_task = page.locator(".column-todo .task-card", has_text="Refactor API Service")
        todo_task.locator("button.btn-next").click()
        page.wait_for_function(
            "() => [...document.querySelectorAll('.column-in_progress .task-title')].some(el => el.textContent.includes('Refactor API Service'))",
            timeout=8000,
        )
        time.sleep(0.4)
        shot(page, "06-task-in-progress.png")

        # ----- move to Done
        wip_task = page.locator(".column-in_progress .task-card", has_text="Refactor API Service")
        wip_task.locator("button.btn-next").click()
        page.wait_for_function(
            "() => [...document.querySelectorAll('.column-done .task-title')].some(el => el.textContent.includes('Refactor API Service'))",
            timeout=8000,
        )
        time.sleep(0.4)
        shot(page, "07-task-in-done.png")

        # ----- delete confirmation (dark), then cancel to keep the board tidy
        done_task = page.locator(".column-done .task-card", has_text="Refactor API Service")
        done_task.locator("button.btn-delete").click()
        time.sleep(0.4)
        shot(page, "08-delete-confirmation.png")
        done_task.locator("button.btn-cancel-delete").click()

        # ----- responsive mobile view (dark)
        mobile = browser.new_page(viewport={"width": 390, "height": 844})
        mobile.goto(FRONTEND_URL, wait_until="networkidle")
        mobile.wait_for_selector(".task-card", timeout=15000)
        time.sleep(0.6)
        shot(mobile, "10-mobile-dark.png")
        mobile.close()

        # Cleanup the extra task created during the flow.
        _, tasks = http("GET", "/tasks")
        for task in tasks["tasks"]:
            if task["title"] in ("Watch Tutorials", "Refactor API Service"):
                http("DELETE", f"/tasks/{task['id']}")

        browser.close()


def capture_database_table():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 500})
        _, tasks = http("GET", "/tasks")
        rows = "".join(
            f"<tr><td>{t['id']}</td><td>{t['title']}</td><td>{t['description']}</td>"
            f"<td>{t['status']}</td></tr>"
            for t in tasks["tasks"]
        )
        html = f"""
        <!doctype html><html><head><meta charset="utf-8"><style>
          body {{ font-family: 'Segoe UI', sans-serif; padding: 28px; background: #f9fafb; }}
          h1 {{ font-size: 20px; margin: 0 0 6px; }}
          p {{ color:#6b7280; font-size: 13px; margin: 0 0 16px; }}
          table {{ border-collapse: collapse; width: 100%; background: #fff; border-radius: 10px;
                    box-shadow: 0 1px 3px rgba(0,0,0,.1); overflow: hidden; }}
          th {{ text-align: left; background: #7C3AED; color: #fff; padding: 10px 14px; font-size: 13px; }}
          td {{ padding: 10px 14px; border-top: 1px solid #e5e7eb; font-size: 13px; }}
          tr:nth-child(even) td {{ background: #f9fafb; }}
        </style></head><body>
          <h1>tasks table — mini_trello database</h1>
          <p>Live data captured from the application database.</p>
          <table>
            <tr><th>id</th><th>title</th><th>description</th><th>status</th></tr>
            {rows}
          </table>
        </body></html>
        """
        page.set_content(html)
        time.sleep(0.3)
        shot(page, "09-database-table.png")
        browser.close()


def capture_api_demo():
    samples = [
        ("GET", "/tasks", None),
        ("POST", "/tasks", json.dumps({"title": "Sample API Task", "description": "Created for the report."})),
    ]
    rendered = []
    for method, path, body in samples:
        if body is not None:
            data = body.encode()
            req = urllib.request.Request(API_URL + path, data=data, method=method)
            req.add_header("Content-Type", "application/json")
        else:
            req = urllib.request.Request(API_URL + path, method=method)
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            content = resp.read().decode()
        rendered.append((method, path, body or "", status, content))

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 640})
        blocks = ""
        for method, path, body, status, content in rendered:
            blocks += f"""
            <div class="req">
              <div class="line"><span class="m {method.lower()}">{method}</span><code>{path}</code></div>
              <pre class="in">{body or "<no body>"}</pre>
              <div class="line">HTTP STATUS <b>{status}</b></div>
              <pre class="out">{json.dumps(json.loads(content), indent=2, ensure_ascii=False)}</pre>
            </div>"""
        html = f"""
        <!doctype html><html><head><meta charset="utf-8"><style>
          body {{ font-family: 'Consolas', 'Segoe UI', monospace; padding: 28px; background: #f9fafb; }}
          h1 {{ font-family:'Segoe UI'; font-size: 20px; margin: 0 0 6px; }}
          p  {{ font-family:'Segoe UI'; color:#6b7280; font-size: 13px; margin: 0 0 16px; }}
          .req {{ background:#fff; border-radius: 10px; box-shadow:0 1px 3px rgba(0,0,0,.1);
                  margin-bottom: 16px; overflow: hidden; }}
          .line {{ padding: 10px 14px; border-bottom: 1px solid #e5e7eb; font-size: 13px; }}
          .m {{ display:inline-block; padding:2px 8px; border-radius:999px; color:#fff; font-size:12px; margin-right:8px; }}
          .get {{ background:#7C3AED; }} .post {{ background:#16a34a; }} .put {{ background:#d97706; }} .delete {{ background:#dc2626; }}
          code {{ color:#374151; }}
          pre {{ margin:0; padding: 10px 14px; font-size: 12px; overflow-x:auto; }}
          pre.in {{ background:#f8fafc; border-bottom: 1px solid #e5e7eb; color:#6b7280; }}
          pre.out {{ background:#f0fdf4; }}
          b {{ color:#16a34a; }}
        </style></head><body>
          <h1>REST API testing — live requests against the running backend</h1>
          <p>Real responses captured from http://127.0.0.1:5000 (equivalent to Postman verification).</p>
          {blocks}
        </body></html>
        """
        page.set_content(html)
        time.sleep(0.3)
        shot(page, "11-api-testing.png")
        browser.close()

    _, created = http("GET", "/tasks")
    for task in created["tasks"]:
        if task["title"] == "Sample API Task":
            http("DELETE", f"/tasks/{task['id']}")


if __name__ == "__main__":
    reset_database()
    capture_ui_flow()
    capture_database_table()
    capture_api_demo()
    print("All screenshots saved to", SCREENSHOT_DIR)