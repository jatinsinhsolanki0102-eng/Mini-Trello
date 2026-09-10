import { useCallback, useEffect, useState } from 'react'
import Header from './components/Header.jsx'
import Board from './components/Board.jsx'
import TaskModal from './components/TaskModal.jsx'
import Login from './components/Login.jsx'
import {
  getTasks,
  createTask,
  updateTask,
  deleteTask,
  login,
  register,
  me,
  getToken,
  setToken,
} from './services/api.js'

const THEME_STORAGE_KEY = 'mini-trello-theme'

function readStoredTheme() {
  try {
    const stored = localStorage.getItem(THEME_STORAGE_KEY)
    return stored === 'light' || stored === 'dark' ? stored : 'dark'
  } catch {
    return 'dark'
  }
}

export default function App() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [modalOpen, setModalOpen] = useState(false)
  const [theme, setTheme] = useState(readStoredTheme)
  const [incomingId, setIncomingId] = useState(null)
  const [user, setUser] = useState(null)
  const [checkingSession, setCheckingSession] = useState(true)

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    try {
      localStorage.setItem(THEME_STORAGE_KEY, theme)
    } catch {
      /* storage unavailable — theme just won't persist */
    }
  }, [theme])

  useEffect(() => {
    let active = true
    async function restoreSession() {
      if (!getToken()) {
        setCheckingSession(false)
        return
      }
      try {
        const data = await me()
        if (active) setUser(data.user)
      } catch {
        setToken(null)
      } finally {
        if (active) setCheckingSession(false)
      }
    }
    restoreSession()
    return () => {
      active = false
    }
  }, [])

  const handleThemeChange = (nextTheme) => {
    setTheme(nextTheme)
  }

  const handleAuth = async (mode, username, password, done) => {
    try {
      const data =
        mode === 'register'
          ? await register(username, password)
          : await login(username, password)
      setToken(data.token)
      setUser(data.user)
      done(null)
    } catch (err) {
      done(err.message)
    }
  }

  const handleLogout = () => {
    setToken(null)
    setUser(null)
    setTasks([])
  }

  const loadTasks = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getTasks()
      setTasks(data.tasks || [])
    } catch {
      setError('Unable to connect to the server. Please try again.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (user) loadTasks()
  }, [user, loadTasks])

  const handleCreateTask = async ({ title, description }) => {
    try {
      const created = await createTask({ title, description })
      setTasks((prev) => [created, ...prev])
      return { ok: true }
    } catch (err) {
      return { ok: false, error: err.message }
    }
  }

  const handleMoveTask = async (taskId, nextStatus) => {
    const previous = tasks
    setTasks((prev) =>
      prev.map((t) => (t.id === taskId ? { ...t, status: nextStatus } : t))
    )
    setIncomingId(taskId)
    try {
      await updateTask(taskId, { status: nextStatus })
    } catch (err) {
      setTasks(previous)
      alert(`Failed to update task: ${err.message}`)
      return false
    }
    return true
  }

  const handleDeleteTask = async (id) => {
    try {
      await deleteTask(id)
      setTasks((prev) => prev.filter((t) => t.id !== id))
      return true
    } catch (err) {
      alert(`Failed to delete task: ${err.message}`)
      return false
    }
  }

  if (checkingSession) {
    return (
      <div className="app-main auth-loading">
        <div className="board-loading" role="status">
          <span className="spinner" aria-hidden="true" />
          Loading...
        </div>
      </div>
    )
  }

  if (!user) {
    return (
      <Login
        theme={theme}
        onThemeChange={handleThemeChange}
        onAuth={handleAuth}
      />
    )
  }

  return (
    <div className="app">
      <Header
        theme={theme}
        onThemeChange={handleThemeChange}
        onCreate={() => setModalOpen(true)}
        username={user.username}
        onLogout={handleLogout}
      />
      <main className="app-main">
        {error && (
          <div className="banner banner-error" role="alert">
            <span>{error}</span>
            <button type="button" onClick={loadTasks}>
              Retry
            </button>
          </div>
        )}
        <Board
          tasks={tasks}
          loading={loading}
          onMove={handleMoveTask}
          onDelete={handleDeleteTask}
          incomingId={incomingId}
        />
      </main>
      {modalOpen && (
        <TaskModal
          onClose={() => setModalOpen(false)}
          onCreate={handleCreateTask}
        />
      )}
    </div>
  )
}