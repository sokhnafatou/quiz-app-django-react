import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchQuizzes } from './api'

export default function QuizList() {
  const [quizzes, setQuizzes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchQuizzes()
      .then(setQuizzes)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="loading">Chargement des quiz…</p>
  if (error) return <p className="error">{error}</p>

  return (
    <div className="quiz-list">
      <h1>Choisissez un quiz</h1>
      {quizzes.length === 0 ? (
        <p>Aucun quiz n'est disponible pour le moment.</p>
      ) : (
        <ul className="quiz-cards">
          {quizzes.map((quiz) => (
            <li key={quiz.id} className="quiz-card">
              <h2>{quiz.title}</h2>
              <p>{quiz.description}</p>
              <span className="quiz-meta">{quiz.questions_count} questions</span>
              <Link to={`/quizzes/${quiz.id}`} className="btn btn-primary">
                Commencer
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
