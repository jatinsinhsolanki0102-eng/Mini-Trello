# Deploying Mini-Trello to Vercel (with Neon Database)

This guide walks you through deploying the **full stack** so your ma'am
can open the app online and tasks REALLY save (no data loss).

---

## What gets deployed where

| Part            | Where                          |
| --------------- | ------------------------------ |
| Frontend (React/Vite) | Vercel static files         |
| Backend (Flask API)   | Vercel serverless function (`api/index.py`) |
| Database        | Neon Postgres (free tier)      |

---

## Step 1 — Create a free Neon database (one time)

1. Go to https://neon.tech → **Sign up** (GitHub or Google account).
2. Create a new project (any name, e.g. `mini-trello`). Choose a region close to you.
3. Click your database name → **Connect**.
4. Copy the **connection string**. It looks like:
   ```
   postgresql://neondb_owner:ABC123...@ep-frosty-12345.eu-central-1.aws.neon.tech/mini-trello?sslmode=require
   ```
   Keep this string — you'll paste it into Vercel in a moment.

> You do NOT need to create tables. The app creates them automatically
> on first request (`db.create_all()`).

---

## Step 2 — Install & log in to Vercel CLI (one time)

Already installed on this machine (v59). Open a terminal in the project folder
and log in:

```bash
vercel login
```

A browser opens → log in / sign up with GitHub. You stay logged in.

Then link the project to your Vercel account:

```bash
vercel link
```

- Answer: **Set up and deploy** → `Mini-Trello` project.
- Scope / team: your account.
- Link to existing project? **No** (create a new one).

---

## Step 3 — Add the database environment variable

```bash
vercel env add DATABASE_URL
```

Two prompts:
1. Value → **paste your Neon connection string** (`postgresql://...?sslmode=require`).
2. Environments → pick **all** (Development, Preview, Production).
   Type `all` and press Enter.

The app automatically converts it for SQLAlchemy (`postgresql+psycopg2://...`).

---

## Step 4 — Add the production flag (optional)

```bash
vercel env add FLASK_DEBUG
```
Value → `0` (disables Flask debug mode in production). Pick environment: `all`.

---

## Step 5 — Deploy to production

```bash
vercel --prod
```

Vercel will:
- Build the frontend (`frontend/dist`)
- Deploy `api/index.py` as the Flask serverless function
- Rewrite `/api/*` requests to the backend
- Serve the app at something like **https://mini-trello-xxxx.vercel.app**

When it finishes, Vercel prints the production URL. Open it → your app is live.

---

## Step 6 — Verify everything works

1. Open the production URL (or the `.vercel.app` link Vercel printed).
2. Create a task → refresh the page → the task is still there (saved in Neon).
3. Move a task with **Next** / drag-and-drop → refresh → still correct.
4. Click the API link to test it directly:
   ```
   https://your-app.vercel.app/api/tasks
   ```
   → returns the JSON list of tasks.

---

## Updating the app later

```bash
# after making changes, just redeploy:
vercel --prod
```

---

## Troubleshooting

- **Blank page / assets 404** → redeploy clean:
  ```bash
  rm -rf frontend/dist .vercel
  vercel --prod
  ```
- **API returns 500** → the DATABASE_URL may be missing or wrong. Re-check:
  ```bash
  vercel env ls
  ```
  and see the latest logs with:
  ```bash
  vercel logs https://your-app.vercel.app/api/tasks
  ```
- **Local dev still works** → yes. Without DATABASE_URL set locally it keeps
  using SQLite (see `README.md`). The `.env.example` files are unchanged.

---

## Files added for deployment

| File                  | Purpose                                   |
| --------------------- | ----------------------------------------- |
| `api/index.py`        | Flask app as Vercel serverless function   |
| `vercel.json`         | Build command, output dir, rewrites, runtime |
| `requirements.txt`    | Python deps for the Vercel function       |
| `backend/app/config.py` | Auto-converts `postgresql://` → `postgresql+psycopg2://` |
| `backend/requirements.txt` | Added `psycopg2-binary` for Postgres  |

> `.vercel/` and `frontend/dist/` are gitignored so secrets never get committed.