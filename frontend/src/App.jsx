import { useCallback, useEffect, useState } from 'react'
import Header from './components/Header.jsx'
import Board from './components/Board.jsx'
import TaskModal from './components/TaskModal.jsx'
import { getTasks, createTask, updateTask, deleteTask } from './services/api.js'

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

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    try {
      localStorage.setItem(THEME_STORAGE_KEY, theme)
    } catch {
      /* storage unavailable — theme just won't persist */
    }
  }, [theme])

  const handleThemeChange = (nextTheme) => {
    setTheme(nextTheme)
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
    loadTasks()
  }, [loadTasks])

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

  return (
    <div className="app">
      <Header
        theme={theme}
        onThemeChange={handleThemeChange}
        onCreate={() => setModalOpen(true)}
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