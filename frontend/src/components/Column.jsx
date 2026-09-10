import { useState } from 'react'
import TaskCard from './TaskCard.jsx'

const STATUS_LABELS = {
  todo: 'To Do',
  in_progress: 'In Progress',
  done: 'Done',
}

export default function Column({ title, status, tasks, onMove, onDelete, incomingId }) {
  const [dragOver, setDragOver] = useState(false)
  const count = tasks.length
  const countLabel = `${count} ${count === 1 ? 'task' : 'tasks'}`

  const handleDragOver = (e) => {
    if (!e.dataTransfer.types.includes('text/plain')) return
    e.preventDefault()
    e.dataTransfer.dropEffect = 'move'
    setDragOver(true)
  }

  const handleDragLeave = (e) => {
    if (e.currentTarget.contains(e.relatedTarget)) return
    setDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const raw = e.dataTransfer.getData('text/plain')
    if (!raw) return
    const taskId = Number(raw)
    if (Number.isNaN(taskId)) return
    onMove(taskId, status)
  }

  const className = [
    'column',
    `column-${status}`,
    dragOver ? 'is-drag-over' : '',
    dragOver && count === 0 ? 'is-drag-over-empty' : '',
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <section
      className={className}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <div className="column-header">
        <div className="column-heading">
          <span className={`status-dot dot-${status}`} aria-hidden="true" />
          <div>
            <h2 className="column-title">{title}</h2>
            <span className="column-subtitle">{countLabel}</span>
          </div>
        </div>
      </div>

      <div className="column-body">
        {count === 0 ? (
          <div className="empty-state">
            <span className="empty-icon" aria-hidden="true">
              &#9633;
            </span>
            <p className="empty-title">No tasks yet</p>
            <p className="empty-hint">{dragOver ? 'Release to drop here' : 'Drag a task here or create one'}</p>
          </div>
        ) : (
          tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={{ ...task, statusLabel: STATUS_LABELS[task.status] }}
              onMove={onMove}
              onDelete={onDelete}
              incoming={task.id === incomingId}
            />
          ))
        )}
      </div>
    </section>
  )
}