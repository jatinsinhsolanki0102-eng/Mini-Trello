export default function ThemeToggle({ theme, onChange }) {
  return (
    <div className="theme-toggle" role="group" aria-label="Color theme">
      <button
        type="button"
        className={theme === 'light' ? 'theme-option active' : 'theme-option'}
        aria-pressed={theme === 'light'}
        onClick={() => onChange('light')}
      >
        <span className="theme-icon" aria-hidden="true">
          ☀
        </span>
        Light
      </button>
      <button
        type="button"
        className={theme === 'dark' ? 'theme-option active' : 'theme-option'}
        aria-pressed={theme === 'dark'}
        onClick={() => onChange('dark')}
      >
        <span className="theme-icon" aria-hidden="true">
          ☾
        </span>
        Dark
      </button>
    </div>
  )
}