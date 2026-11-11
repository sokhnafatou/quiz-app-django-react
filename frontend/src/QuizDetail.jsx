import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fetchQuiz, submitQuiz } from './api'
import { useAuth } from './AuthContext'

export default function QuizDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const [quiz, setQuiz] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [currentIndex, setCurrentIndex] = useState(0)
  const [answers, setAnswers] = useState({}) // { [questionId]: choiceId }
  const [result, setResult] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    fetchQuiz(id)
      .then(setQuiz)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <p className="loading">Chargement du quiz…</p>
  if (error) return <p className="error">{error}</p>
  if (!quiz) return <p>Quiz introuvable.</p>

  if (result) {
    const total = quiz.questions.length
    const pct = total ? Math.round((result.score / total) * 100) : 0
    return (
      <div className="result">
        <h1>Quiz terminé !</h1>
        <p className="result-quiz">{quiz.title}</p>
        <div className="result-score">
          <span className="result-score-value">{result.score}</span>
          <span className="result-score-total"> / {total}</span>
        </div>
        <p className="result-pct">{pct}% de bonnes réponses</p>
        <div className="result-actions">
          <Link to="/quizzes" className="btn btn-outline">
            Autres quiz
          </Link>
          <Link to="/history" className="btn btn-primary">
            Mes scores
          </Link>
        </div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="auth-required">
        <h1>Connexion requise</h1>
        <p>Vous devez être connecté pour répondre à un quiz et enregistrer votre score.</p>
        <div className="result-actions">
          <Link to="/login" className="btn btn-primary">
            Se connecter
          </Link>
          <Link to="/register" className="btn btn-outline">
            Créer un compte
          </Link>
        </div>
      </div>
    )
  }

  const question = quiz.questions[currentIndex]
  const total = quiz.questions.length
  const selectedChoice = answers[question.id]

  function selectChoice(choiceId) {
    setAnswers({ ...answers, [question.id]: choiceId })
  }

  function next() {
    if (currentIndex < total - 1) setCurrentIndex(currentIndex + 1)
  }

  function prev() {
    if (currentIndex > 0) setCurrentIndex(currentIndex - 1)
  }

  async function handleSubmit() {
    setSubmitting(true)
    setError('')
    const payload = Object.entries(answers).map(([questionId, choiceId]) => ({
      question_id: Number(questionId),
      choice_id: choiceId,
    }))
    try {
      const res = await submitQuiz(id, payload)
      setResult(res)
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  const answeredCount = Object.keys(answers).length
  const allAnswered = answeredCount === total

  return (
    <div className="quiz-detail">
      <Link to="/quizzes" className="back-link">
        ← Retour aux quiz
      </Link>
      <h1>{quiz.title}</h1>
      <p className="quiz-progress">
        Question {currentIndex + 1} / {total}
      </p>
      <div className="progress-bar">
        <div
          className="progress-bar-fill"
          style={{ width: `${((currentIndex + 1) / total) * 100}%` }}
        />
      </div>

      <div className="question">
        <h2>{question.text}</h2>
        <ul className="choices">
          {question.choices.map((choice) => (
            <li key={choice.id}>
              <label
                className={`choice ${
                  selectedChoice === choice.id ? 'choice-selected' : ''
                }`}
              >
                <input
                  type="radio"
                  name={`q-${question.id}`}
                  checked={selectedChoice === choice.id}
                  onChange={() => selectChoice(choice.id)}
                />
                <span>{choice.text}</span>
              </label>
            </li>
          ))}
        </ul>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="quiz-nav">
        <button onClick={prev} disabled={currentIndex === 0} className="btn btn-outline">
          Précédent
        </button>
        {currentIndex < total - 1 ? (
          <button onClick={next} disabled={!selectedChoice} className="btn btn-primary">
            Suivant
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={!allAnswered || submitting}
            className="btn btn-primary"
          >
            {submitting ? 'Envoi…' : 'Terminer le quiz'}
          </button>
        )}
      </div>
    </div>
  )
}
