import { useState, type FormEvent } from "react"
import { Link, Navigate } from "react-router"
import { useAuth } from "../auth/AuthProvider"

interface AccountPageProps {
  mode: "login" | "signup"
}

function AccountPage({ mode }: AccountPageProps) {
  const isLogin = mode === "login"
  const { user, isLoading, signIn, signUp } = useAuth()
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsSubmitting(true)
    setError(null)

    try {
      if (isLogin) {
        await signIn({ email, password })
      } else {
        await signUp({ name, email, password })
      }
    } catch (cause: unknown) {
      setError(cause instanceof Error ? cause.message : "Unable to complete your request.")
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isLoading) return <p className="account-status">Checking your session...</p>
  if (user) return <Navigate to="/events" replace />

  return (
    <section className="account-page">
      <p className="eyebrow">Your NC+1 account</p>
      <h1>{isLogin ? "Welcome back." : "Come join us."}</h1>
      <p className="account-description">
        {isLogin
          ? "Sign in to keep your plans and RSVPs together."
          : "Create an account to start making plans."}
      </p>
      <form className="account-form" onSubmit={handleSubmit}>
        {!isLogin && (
          <label className="account-field">
            <span>Name</span>
            <input
              autoComplete="name"
              name="name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              required
            />
          </label>
        )}
        <label className="account-field">
          <span>Email</span>
          <input
            autoComplete="email"
            name="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </label>
        <label className="account-field">
          <span>Password</span>
          <input
            autoComplete={isLogin ? "current-password" : "new-password"}
            name="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </label>
        {error && <p className="account-error" role="alert">{error}</p>}
        <button className="account-submit" type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Please wait..." : isLogin ? "Sign in" : "Create account"}
        </button>
      </form>
      <p className="account-switch">
        {isLogin ? "New around here?" : "Already have an account?"}{" "}
        <Link to={isLogin ? "/signup" : "/login"}>
          {isLogin ? "Sign up" : "Log in"}
        </Link>
      </p>
    </section>
  )
}

export default AccountPage