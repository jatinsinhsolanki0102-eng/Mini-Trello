import ThemeToggle from './ThemeToggle.jsx'

export default function Header({ theme, onThemeChange, onCreate, username, onLogout }) {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="header-brand">
          <span className="logo" aria-hidden="true">
            <i className="logo-bar bar-1" />
            <i className="logo-bar bar-2" />
            <i className="logo-bar bar-3" />
          </span>
          <div className="brand-text">
            <h1 className="header-title">Mini-Trello</h1>
            <p className="header-subtitle">Simple Kanban Task Management</p>
          </div>
        </div>

        <div className="header-actions">
          <span className="header-user">{username}</span>
          <ThemeToggle theme={theme} onChange={onThemeChange} />
          <button
            type="button"
            className="btn btn-primary btn-create"
            onClick={onCreate}
          >
            <span className="btn-plus" aria-hidden="true">
              +
            </span>
            Create New Task
          </button>
          <button
            type="button"
            className="btn btn-ghost btn-logout"
            onClick={onLogout}
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  )
}