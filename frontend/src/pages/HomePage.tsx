import { Link } from "react-router"


function HomePage() {
  return (
    <section className="placeholder-page">
      <p className="eyebrow">404 / Not found</p>
      <h1>This page isn’t here.</h1>
      <Link className="text-link" to="/">
        Back to home
      </Link>
    </section>
  )
}

export default HomePage