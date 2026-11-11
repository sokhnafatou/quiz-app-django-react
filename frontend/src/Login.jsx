import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from './AuthContext'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await login(form.username, form.password)
      navigate('/quizzes')
    } catch (err) {
      setError(err.message || 'Connexion impossible')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="auth">
      <h1>Connexion</h1>
      <form onSubmit={handleSubmit} className="auth-form">
        <label>
          Nom d'utilisateur
          <input
            type="text"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            required
            autoComplete="username"
          />
        </label>
        <label>
          Mot de passe
          <input
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
            autoComplete="current-password"
          />
        </label>
        {error && <p className="error">{error}</p>}
        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? 'Connexion…' : 'Se connecter'}
        </button>
      </form>
    </div>
  )
}
