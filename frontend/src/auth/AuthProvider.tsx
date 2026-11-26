import { createContext, useContext, useEffect, useState, type PropsWithChildren } from "react"
import { getCurrentUser, login, register } from "../api/auth"
import { AUTH_EXPIRED_EVENT, clearAccessToken, getAccessToken, saveAccessToken } from "./token"
import type { AuthUser, LoginCredentials, RegisterDetails } from "../types/auth"

interface AuthContextValue {
  user: AuthUser | null
  isLoading: boolean
  signIn: (credentials: LoginCredentials) => Promise<void>
  signUp: (details: RegisterDetails) => Promise<void>
  signOut: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: PropsWithChildren) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    let active = true

    function handleAuthExpired() {
      setUser(null)
      setIsLoading(false)
    }

    window.addEventListener(AUTH_EXPIRED_EVENT, handleAuthExpired)

    async function restoreSession() {
      if (!getAccessToken()) {
        setIsLoading(false)
        return
      }

      try {
        const currentUser = await getCurrentUser()
        if (active) setUser(currentUser)
      } catch {
        if (active) setUser(null)
      } finally {
        if (active) setIsLoading(false)
      }
    }

    void restoreSession()

    return () => {
      active = false
      window.removeEventListener(AUTH_EXPIRED_EVENT, handleAuthExpired)
    }
  }, [])

  async function signIn(credentials: LoginCredentials) {
    const result = await login(credentials)
    saveAccessToken(result.access_token)

    try {
      setUser(await getCurrentUser())
    } catch (error) {
      clearAccessToken()
      setUser(null)
      throw error
    }
  }

  async function signUp(details: RegisterDetails) {
    await register(details)
    await signIn({ email: details.email, password: details.password })
  }

  function signOut() {
    clearAccessToken()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (!context) throw new Error("useAuth must be used inside AuthProvider")
  return context
}