import { Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider, useAuth } from './AuthContext'
import History from './History'
import Home from './Home'
import Login from './Login'
import Navbar from './Navbar'
import QuizDetail from './QuizDetail'
import QuizList from './QuizList'
import Register from './Register'

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <p className="loading">Chargement…</p>
  if (!user) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <AuthProvider>
      <Navbar />
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/quizzes" element={<QuizList />} />
          <Route path="/quizzes/:id" element={<QuizDetail />} />
          <Route
            path="/history"
            element={
              <ProtectedRoute>
                <History />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </AuthProvider>
  )
}
