import { useState } from 'react'
import ThemeToggle from './ThemeToggle.jsx'

export default function Login({ theme, onThemeChange, onAuth }) {
  const [mode, setMode] = useState('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    if (!username.trim() || !password) {
      setError('Please enter a username and password.')
      return
    }
    setSubmitting(true)
    onAuth(mode, username.trim(), password, (err) => {
      setError(err)
      setSubmitting(false)
    })
  }

  const switchMode = (next) => {
    setMode(next)
    setError(null)
  }

  return (
    <div className="auth-page">
      <div className="auth-box">
        <div className="auth-brand">
          <span className="logo" aria-hidden="true">
            <i className="logo-bar bar-1" />
            <i className="logo-bar bar-2" />
            <i className="logo-bar bar-3" />
          </span>
          <div className="brand-text">
            <h1 className="auth-title">Mini-Trello</h1>
            <p className="auth-subtitle">
              {mode === 'login'
                ? 'Log in to your personal kanban board'
                : 'Create your own private kanban board'}
            </p>
          </div>
        </div>

        <form className="auth-form" onSubmit={handleSubmit} noValidate>
          <div className="field">
            <label className="field-label" htmlFor="auth-username">
              Username
            </label>
            <input
              id="auth-username"
              className="input"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. jatin"
              autoComplete="username"
              autoFocus
            />
          </div>

          <div className="field">
            <label className="field-label" htmlFor="auth-password">
              Password
            </label>
            <input
              id="auth-password"
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="At least 6 characters"
              autoComplete={
                mode === 'login' ? 'current-password' : 'new-password'
              }
            />
          </div>

          {error && (
            <div className="banner banner-error auth-error" role="alert">
              <span>{error}</span>
            </div>
          )}

          <button
            type="submit"
            className="btn btn-primary btn-auth-submit"
            disabled={submitting}
          >
            {submitting
              ? 'Please wait...'
              : mode === 'login'
                ? 'Log In'
                : 'Create Account'}
          </button>
        </form>

        <div className="auth-footer">
          {mode === 'login' ? (
            <>
              New here?{' '}
              <button
                type="button"
                className="link-button"
                onClick={() => switchMode('register')}
              >
                Create an account
              </button>
            </>
          ) : (
            <>
              Already have an account?{' '}
              <button
                type="button"
                className="link-button"
                onClick={() => switchMode('login')}
              >
                Log in
              </button>
            </>
          )}
        </div>
      </div>

      <div className="auth-theme-toggle">
        <ThemeToggle theme={theme} onChange={onThemeChange} />
      </div>
    </div>
  )
}