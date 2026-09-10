# Deploying Mini-Trello to Vercel (with Supabase Database)

This guide walks you through deploying the **full stack** so your ma'am
can open the app online and tasks REALLY save (no data loss).

---

## What gets deployed where

| Part            | Where                          |
| --------------- | ------------------------------ |
| Frontend (React/Vite) | Vercel static files         |
| Backend (Flask API)   | Vercel serverless function (`api/index.py`) |
| Database        | Supabase Postgres (free tier)  |

---

## Step 1 — Create a free Supabase database (one time, ~3 min)

1. Go to https://supabase.com → **Start your project**.
2. Sign in with GitHub (fastest).
3. Click **New project**:
   - **Name**: `mini-trello`
   - **Database password**: create one and **save it somewhere** (you will
     need it for the connection string below).
   - **Region**: pick the closest one to you (e.g. `ap-south-1` for India).
   - **Plan**: Free.
   - Click **Create new project** and wait ~1 minute for it to be ready.
4. In the project, go to **Connect** (top right) → it shows connection
   strings. Choose **Session pooler** in the "Port" dropdown.

   Copy the string — it looks like this:
   ```
   postgresql://postgres.abcdefghijklmnop:[YOUR-PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:5432/postgres
   ```

5. Replace `[YOUR-PASSWORD]` with the database password you saved in step 3.
   Paste this FULL string somewhere safe — you'll give it to Vercel in Step 3.

> The app creates the tables automatically on first request, so you do NOT
> need to run any SQL or create anything inside Supabase.

---

## Step 2 — Log in & link Vercel (one time)

The Vercel CLI is already installed on this machine. Open a terminal in the
project folder and log in:

```bash
vercel login
```

- A browser opens → **Continue with GitHub** → authorize.
- Return to the terminal — it automatically finishes logging in.

Then create a link between this folder and your Vercel account:

```bash
vercel link
```

- Answer: **Set up and deploy** → project name stays as the folder name
  (`mini-trello`) or type any name you like.
- Scope/team → your account.
- "Link to existing project?" → **No**.

---

## Step 3 — Add the database environment variable

```bash
vercel env add DATABASE_URL
```

The CLI asks you to paste the value:

1. **Value** → right-click / Ctrl+V to paste your full Supabase string
   (`postgresql://...pooler.supabase.com:5432/postgres`). Press Enter.
2. **Which Environments** → select **all** (Development, Preview,
   Production) — you can type `3` if shown as a number list, or pick each.

Then add a flag to turn off Flask debug mode in production:

```bash
vercel env add FLASK_DEBUG
```
- Value → `0`
- Environments → **all**

Verify both are stored:

```bash
vercel env ls
```

---

## Step 4 — Deploy to production

```bash
vercel --prod
```

Vercel will:
- Build the frontend (`frontend/dist`)
- Install Python deps (`requirements.txt`)
- Run the Flask app from `api/index.py` as a serverless function
- Rewrite `/api/*` requests to the backend
- Print your live URL at the end, like **https://mini-trello-jatinsinh.vercel.app**

> First deploy takes 1–3 minutes. Later ones are much faster.

---

## Step 5 — Verify everything works

1. Open the URL Vercel printed (or find it later with `vercel projects ls`).
2. Create a task → refresh the page → the task is still there (it's now
   saved in Supabase).
3. Move a task with **Next** / drag-and-drop → refresh → still correct.
4. Check the API directly:
   ```
   https://your-app.vercel.app/api/tasks
   ```
   → returns the JSON list of tasks.
5. To prove it's really saving: open the Supabase dashboard →
   **Table editor** → you will see your tasks in the `task` table.

---

## Sending it to your ma'am

Reply to her with:

> The project is now fully deployed and live. Open this link:
> https://your-app.vercel.app
> You can create, edit, delete, and drag-and-drop tasks — everything saves
> to a real online database (Supabase Postgres), so no data is lost.

---

## Updating the app later

```bash
# after making any code changes, just redeploy:
vercel --prod
```

---

## Troubleshooting

- **API returns 500** → the DATABASE_URL value may have a typo or the
  password wasn't replaced. Re-check with `vercel env ls`, re-add with
  `vercel env remove DATABASE_URL` then `vercel env add DATABASE_URL`.
- **Blank page / assets 404** → clean rebuild:
  ```bash
  rm -rf frontend/dist .vercel
  vercel --prod
  ```
- **Latest logs / errors**:
  ```bash
  vercel logs https://your-app.vercel.app/api/tasks
  ```
- **Local dev still works** → yes. Without DATABASE_URL set locally it keeps
  using SQLite (see `README.md`). `.env.example` files are unchanged.

---

## Files used for deployment

| File                  | Purpose                                   |
| --------------------- | ----------------------------------------- |
| `api/index.py`        | Flask app as Vercel serverless function   |
| `vercel.json`         | Build command, output dir, rewrites, runtime |
| `requirements.txt`    | Python deps for the Vercel function       |
| `backend/app/config.py` | Auto-converts `postgresql://` → SQLAlchemy URL and strips `pgbouncer=true` |
| `backend/requirements.txt` | Added `psycopg2-binary` for Postgres  |

> `.vercel/` and `frontend/dist/` are gitignored so secrets never get committed.