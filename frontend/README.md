# Mini-Trello Frontend

React + Vite frontend for the Mini-Trello Kanban board.

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

The dev server runs on `http://localhost:5173`. API calls to `/api/*` are
proxied to the Flask backend on `http://127.0.0.1:5000` (see `vite.config.js`).
Start the backend first — see the root `README.md`.

## Production build

```bash
npm run build
npm run preview
```

When serving the built app separately from the Vite dev server, copy
`.env.example` to `.env` and set `VITE_API_URL` to the backend URL
(e.g. `http://localhost:5000/api`), then rebuild.

## Project structure

```
frontend/
├── index.html
├── package.json
├── vite.config.js
├── .env.example
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── services/api.js          # centralized REST client
    ├── components/
    │   ├── Header.jsx
    │   ├── Board.jsx
    │   ├── Column.jsx
    │   ├── TaskCard.jsx
    │   └── TaskModal.jsx
    └── styles/styles.css
```