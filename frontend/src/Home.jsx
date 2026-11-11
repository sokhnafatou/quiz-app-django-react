import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="home">
      <h1>Bienvenue sur QuizEdu</h1>
      <p className="home-subtitle">
        Une petite application de quiz éducatifs pour apprendre en s'amusant.
      </p>
      <div className="home-cards">
        <div className="home-card">
          <h2>Capitales d'Afrique</h2>
          <p>Testez vos connaissances sur les capitales du continent africain.</p>
        </div>
        <div className="home-card">
          <h2>Bases de Python</h2>
          <p>Révisez les fondamentaux du langage Python en quelques questions.</p>
        </div>
      </div>
      <Link to="/quizzes" className="btn btn-primary home-cta">
        Voir les quiz
      </Link>
    </div>
  )
}
