/**
 * Centralized API service for Mini-Trello frontend.
 * All HTTP calls to the backend go through this module.
 *
 * Base URL resolution:
 *  1. VITE_API_URL from frontend/.env if set
 *  2. "/api" (used in development via the Vite proxy to the Flask server)
 */
const API_BASE = import.meta.env.VITE_API_URL || '/api';

const TOKEN_KEY = 'mini-trello-token';

export function getToken() {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

export function setToken(token) {
  try {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
    } else {
      localStorage.removeItem(TOKEN_KEY);
    }
  } catch {
    /* storage unavailable — auth won't persist across reloads */
  }
}

function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    ...options,
  });

  let body = null;
  const text = await response.text();
  if (text) {
    try {
      body = JSON.parse(text);
    } catch {
      body = null;
    }
  }

  if (!response.ok) {
    if (response.status === 401 && getToken()) {
      setToken(null);
    }
    const message =
      (body && body.error) || `Request failed with status ${response.status}`;
    const error = new Error(message);
    error.status = response.status;
    error.body = body;
    throw error;
  }

  return body;
}

export function register(username, password) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
}

export function login(username, password) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
}

export function me() {
  return request('/auth/me');
}

export function getTasks() {
  return request('/tasks');
}

export function createTask(payload) {
  return request('/tasks', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function updateTask(id, payload) {
  return request(`/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  });
}

export function deleteTask(id) {
  return request(`/tasks/${id}`, { method: 'DELETE' });
}