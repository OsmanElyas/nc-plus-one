import { Link, NavLink } from "react-router"

function SiteHeader() {
  return (
    <header className="site-header">
      <div className="header-inner">
        <Link className="brand" to="/" aria-label="NC Plus One home">
          <span className="brand-mark">+1</span>
          <span className="brand-name">NC Plus One</span>
        </Link>
        <nav className="main-nav" aria-label="Main navigation">
          <NavLink to="/events">Explore</NavLink>
          <div className="account-nav">
            <NavLink className="login-link" to="/login">
              Log in
            </NavLink>
            <NavLink className="signup-link" to="/signup">
              Sign up
            </NavLink>
          </div>
        </nav>
      </div>
    </header>
  )
}

export default SiteHeader