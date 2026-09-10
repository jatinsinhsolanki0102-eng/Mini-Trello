import Column from './Column.jsx'

const COLUMNS = [
  { key: 'todo', title: 'To Do', status: 'todo' },
  { key: 'in_progress', title: 'In Progress', status: 'in_progress' },
  { key: 'done', title: 'Done', status: 'done' },
]

export default function Board({ tasks, loading, onMove, onDelete, incomingId }) {
  if (loading) {
    return (
      <div className="board-loading" role="status">
        <span className="spinner" aria-hidden="true" />
        Loading tasks...
      </div>
    )
  }

  return (
    <div className="board">
      {COLUMNS.map((column) => {
        const columnTasks = tasks.filter((t) => t.status === column.status)
        return (
          <Column
            key={column.key}
            title={column.title}
            status={column.status}
            tasks={columnTasks}
            onMove={onMove}
            onDelete={onDelete}
            incomingId={incomingId}
          />
        )
      })}
    </div>
  )
}