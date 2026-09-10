import { useEffect, useRef, useState } from 'react'

export default function TaskModal({ onClose, onCreate }) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [serverError, setServerError] = useState(null)
  const titleRef = useRef(null)

  useEffect(() => {
    titleRef.current && titleRef.current.focus()
  }, [])

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        onClose()
      }
    }
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [onClose])

  const validate = () => {
    const nextErrors = {}
    if (!title.trim()) {
      nextErrors.title = 'Title is required.'
    }
    if (!description.trim()) {
      nextErrors.description = 'Description is required.'
    }
    setErrors(nextErrors)
    return Object.keys(nextErrors).length === 0
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setServerError(null)

    const trimmedTitle = title.trim()
    const trimmedDescription = description.trim()

    if (!validate(trimmedTitle, trimmedDescription)) {
      return
    }

    setSubmitting(true)
    const result = await onCreate({
      title: trimmedTitle,
      description: trimmedDescription,
    })
    setSubmitting(false)

    if (result.ok) {
      setTitle('')
      setDescription('')
      onClose()
    } else {
      setServerError(result.error || 'Something went wrong. Please try again.')
    }
  }

  return (
    <div
      className="modal-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      onClick={(event) => {
        if (event.target === event.currentTarget) {
          onClose()
        }
      }}
    >
      <div className="modal">
        <div className="modal-header">
          <h2 id="modal-title" className="modal-title">
            Create New Task
          </h2>
          <button
            type="button"
            className="btn-icon modal-close"
            onClick={onClose}
            aria-label="Close"
          >
            &times;
          </button>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <div className="field">
            <label className="field-label" htmlFor="task-title">
              Title <span className="req">*</span>
            </label>
            <input
              id="task-title"
              ref={titleRef}
              type="text"
              value={title}
              placeholder="e.g. Create Database"
              onChange={(e) => setTitle(e.target.value)}
              className={errors.title ? 'input input-error' : 'input'}
            />
            {errors.title && <span className="field-error">{errors.title}</span>}
          </div>

          <div className="field">
            <label className="field-label" htmlFor="task-description">
              Description <span className="req">*</span>
            </label>
            <textarea
              id="task-description"
              rows="4"
              value={description}
              placeholder="e.g. Design the MySQL schema for tasks."
              onChange={(e) => setDescription(e.target.value)}
              className={errors.description ? 'input textarea input-error' : 'input textarea'}
            />
            {errors.description && (
              <span className="field-error">{errors.description}</span>
            )}
          </div>

          {serverError && (
            <div className="banner banner-error" role="alert">
              {serverError}
            </div>
          )}

          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? 'Adding...' : 'Create Task'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}