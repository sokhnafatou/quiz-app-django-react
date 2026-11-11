// Client HTTP léger pour l'API Django REST.
// Gère le token JWT (stocké dans localStorage) et les erreurs HTTP.

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export function getToken() {
  return localStorage.getItem('access_token')
}

export function setToken(token) {
  if (token) localStorage.setItem('access_token', token)
  else localStorage.removeItem('access_token')
}

async function request(path, { method = 'GET', body, auth = true } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  if (auth) {
    const token = getToken()
    if (token) headers.Authorization = `Bearer ${token}`
  }
  const res = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) {
    let detail = `Erreur HTTP ${res.status}`
    try {
      const data = await res.json()
      detail = data.detail || data
    } catch {
      // réponse non-JSON
    }
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail))
  }
  if (res.status === 204) return null
  return res.json()
}

// --- Authentification ---

export async function register(username, email, password) {
  const data = await request('/api/auth/register/', {
    method: 'POST',
    body: { username, email, password },
    auth: false,
  })
  return login(username, password).then(() => data)
}

export async function login(username, password) {
  const data = await request('/api/auth/login/', {
    method: 'POST',
    body: { username, password },
    auth: false,
  })
  setToken(data.access)
  localStorage.setItem('refresh_token', data.refresh)
  return data
}

export function logout() {
  setToken(null)
  localStorage.removeItem('refresh_token')
}

export async function fetchMe() {
  return request('/api/auth/me/')
}

// --- Quiz ---

export async function fetchQuizzes() {
  return request('/api/quizzes/')
}

export async function fetchQuiz(id) {
  return request(`/api/quizzes/${id}/`)
}

export async function submitQuiz(id, answers) {
  return request(`/api/quizzes/${id}/submit/`, {
    method: 'POST',
    body: { answers },
  })
}

export async function fetchMySubmissions() {
  return request('/api/quizzes/submissions/')
}
