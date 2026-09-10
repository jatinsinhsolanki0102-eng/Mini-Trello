import { useEffect, useRef, useState } from 'react'

const NEXT_STATUS = {
  todo: 'in_progress',
  in_progress: 'done',
}

const PREVIOUS_STATUS = {
  in_progress: 'todo',
  done: 'in_progress',
}

function TrashIcon() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M3 6h18" />
      <path d="M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2" />
      <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
      <path d="M10 11v6" />
      <path d="M14 11v6" />
    </svg>
  )
}

export default function TaskCard({ task, onMove, onDelete, incoming }) {
  const [confirming, setConfirming] = useState(false)
  const [leaving, setLeaving] = useState(false)
  const [dragging, setDragging] = useState(false)
  const moveTimer = useRef(null)

  useEffect(
    () => () => {
      if (moveTimer.current) clearTimeout(moveTimer.current)
    },
    []
  )

  const canGoNext = Boolean(NEXT_STATUS[task.status])
  const canGoPrevious = Boolean(PREVIOUS_STATUS[task.status])

  const handleMove = (nextStatus) => {
    if (moveTimer.current) return
    setLeaving(true)
    moveTimer.current = setTimeout(() => {
      onMove(task.id, nextStatus)
    }, 0)
  }

  const handleDragStart = (e) => {
    setDragging(true)
    e.dataTransfer.effectAllowed = 'move'
    e.dataTransfer.setData('text/plain', String(task.id))
  }

  const handleDragEnd = () => setDragging(false)

  const handleDeleteClick = () => setConfirming(true)
  const handleCancelDelete = () => setConfirming(false)
  const handleConfirmDelete = () => {
    setConfirming(false)
    onDelete(task.id)
  }

  const cardClass = [
    'task-card',
    leaving ? 'task-card--leaving' : '',
    dragging ? 'is-dragging' : '',
    incoming && !leaving ? 'task-card--in' : '',
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <article
      className={cardClass}
      draggable
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      <div className="task-head">
        <h3 className="task-title">{task.title}</h3>
        <button
          type="button"
          className="btn-icon btn-delete"
          onClick={handleDeleteClick}
          aria-label={`Delete task "${task.title}"`}
          title="Delete task"
        >
          <TrashIcon />
        </button>
      </div>
      <p className="task-description">{task.description}</p>

      <div className="task-meta">
        <span className={`task-status status-${task.status}`}>
          {task.statusLabel}
        </span>
      </div>

      {confirming ? (
        <div className="confirm-box" role="alertdialog" aria-label="Confirm delete">
          <p className="confirm-text">Are you sure you want to delete this task?</p>
          <div className="task-actions">
            <button
              type="button"
              className="btn btn-secondary btn-cancel-delete"
              onClick={handleCancelDelete}
            >
              Cancel
            </button>
            <button
              type="button"
              className="btn btn-danger-solid btn-confirm-delete"
              onClick={handleConfirmDelete}
            >
              Delete
            </button>
          </div>
        </div>
      ) : (
        <div className="task-actions">
          {canGoPrevious && (
            <button
              type="button"
              className="btn btn-ghost btn-previous"
              onClick={() => handleMove(PREVIOUS_STATUS[task.status])}
            >
              &larr; Previous
            </button>
          )}
          {canGoNext && (
            <button
              type="button"
              className="btn btn-ghost btn-next"
              onClick={() => handleMove(NEXT_STATUS[task.status])}
            >
              Next &rarr;
            </button>
          )}
        </div>
      )}
    </article>
  )
}