import { createContext, useContext, useEffect, useState } from 'react'
import {
  fetchMe,
  getToken,
  login as apiLogin,
  logout as apiLogout,
  register as apiRegister,
} from './api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!getToken()) {
      setLoading(false)
      return
    }
    fetchMe()
      .then(setUser)
      .catch(() => {
        apiLogout()
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [])

  async function login(username, password) {
    await apiLogin(username, password)
    const me = await fetchMe()
    setUser(me)
    return me
  }

  async function register(username, email, password) {
    await apiRegister(username, email, password)
    const me = await fetchMe()
    setUser(me)
    return me
  }

  function logout() {
    apiLogout()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth doit être utilisé dans un AuthProvider')
  return ctx
}
