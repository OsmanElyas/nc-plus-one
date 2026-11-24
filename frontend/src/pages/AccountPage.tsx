import { Link } from "react-router"

interface AccountPageProps {
  mode: "login" | "signup"
}

function AccountPage({ mode }: AccountPageProps) {
  const isLogin = mode === "login"

  return (
    <section className="account-page">
      <p className="eyebrow">Your NC+1 account</p>
      <h1>{isLogin ? "Welcome back." : "Come join us."}</h1>
      <p className="account-description">
        {isLogin
          ? "The sign-in form will be added here."
          : "The account creation form will be added here."}
      </p>
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