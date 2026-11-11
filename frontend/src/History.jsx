import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchMySubmissions } from './api'

export default function History() {
  const [submissions, setSubmissions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchMySubmissions()
      .then(setSubmissions)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="loading">Chargement de l'historique…</p>
  if (error) return <p className="error">{error}</p>

  return (
    <div className="history">
      <h1>Mes scores</h1>
      {submissions.length === 0 ? (
        <div className="empty">
          <p>Vous n'avez pas encore passé de quiz.</p>
          <Link to="/quizzes" className="btn btn-primary">
            Passer un quiz
          </Link>
        </div>
      ) : (
        <table className="history-table">
          <thead>
            <tr>
              <th>Quiz</th>
              <th>Score</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {submissions.map((s) => (
              <tr key={s.id}>
                <td>Quiz #{s.quiz}</td>
                <td>{s.score}</td>
                <td>{new Date(s.submitted_at).toLocaleString('fr-FR')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
