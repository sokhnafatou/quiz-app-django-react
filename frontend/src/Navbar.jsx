import { Link, NavLink } from 'react-router-dom'
import { useAuth } from './AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        QuizEdu
      </Link>
      <div className="navbar-links">
        <NavLink to="/" end className={({ isActive }) => (isActive ? 'active' : '')}>
          Accueil
        </NavLink>
        <NavLink to="/quizzes" className={({ isActive }) => (isActive ? 'active' : '')}>
          Quiz
        </NavLink>
        {user && (
          <NavLink to="/history" className={({ isActive }) => (isActive ? 'active' : '')}>
            Mes scores
          </NavLink>
        )}
      </div>
      <div className="navbar-auth">
        {user ? (
          <>
            <span className="navbar-user">Bonjour, {user.username}</span>
            <button onClick={logout} className="btn btn-outline">
              Déconnexion
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn btn-outline">
              Connexion
            </Link>
            <Link to="/register" className="btn btn-primary">
              Inscription
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}
