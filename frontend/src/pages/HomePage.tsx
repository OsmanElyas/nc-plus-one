import { Link } from "react-router"
import { useAuth } from "../auth/AuthProvider"
import { useEvents } from "../hooks/useEvents"

function HomePage() {
  const { user, isLoading: isAuthLoading } = useAuth()
  const { events, isLoading, error } = useEvents()
  const today = new Date()
  const todayKey = [today.getFullYear(), String(today.getMonth() + 1).padStart(2, "0"), String(today.getDate()).padStart(2, "0")].join("-")
  const nextEvent = events
    .filter((event) => event.starts_at.slice(0, 10) >= todayKey)
    .sort((first, second) => first.starts_at.localeCompare(second.starts_at))[0]

  const nextEventDate = nextEvent
    ? new Date(/^\d{4}-\d{2}-\d{2}$/.test(nextEvent.starts_at) ? `${nextEvent.starts_at}T12:00:00` : nextEvent.starts_at)
    : null

  return (
    <div className="home-page">
      <section className="home-hero">
        <div className="hero-copy">
          <p className="eyebrow">Good plans start together</p>
          <h1>Find your next event. Bring someone along.</h1>
          <p className="hero-description">
            Discover meetups, workshops, and gatherings around shared interests. There’s always room for one more.
          </p>
          <div className="hero-actions">
            <Link className="button button-coral" to="/events">Explore events</Link>
            {!isAuthLoading && (user ? (
              <Link className="button button-outline" to="/my-events">See my events</Link>
            ) : (
              <Link className="button button-outline" to="/signup">Create an account</Link>
            ))}
          </div>
          <p className="hero-footnote">Browse freely. Sign in when you’re ready to RSVP.</p>
        </div>

        <aside className="hero-artwork" aria-label="Featured upcoming event">
          <span className="artwork-label">NEXT UP</span>
          {isLoading ? (
            <p className="home-feature-message">Finding the next event...</p>
          ) : error ? (
            <p className="home-feature-message">Explore the full list to see what’s on.</p>
          ) : nextEvent && nextEventDate ? (
            <div className="home-feature-event">
              <time className="home-feature-date" dateTime={nextEvent.starts_at}>
                <span>{new Intl.DateTimeFormat("en-GB", { month: "short" }).format(nextEventDate)}</span>
                <strong>{new Intl.DateTimeFormat("en-GB", { day: "2-digit" }).format(nextEventDate)}</strong>
                <span>{new Intl.DateTimeFormat("en-GB", { year: "numeric" }).format(nextEventDate)}</span>
              </time>
              <div className="home-feature-copy">
                <p>{nextEvent.location}</p>
                <h2>{nextEvent.title}</h2>
              </div>
              <Link className="home-feature-link" to={`/events/${nextEvent.id}`}>
                View event details <span aria-hidden="true">&rarr;</span>
              </Link>
            </div>
          ) : (
            <div className="home-feature-empty">
              <strong>Make a plan.</strong>
              <span>Find a new place to start.</span>
              <Link to="/events">Explore events <span aria-hidden="true">&rarr;</span></Link>
            </div>
          )}
        </aside>
      </section>

      <section className="starting-section" aria-labelledby="home-start-heading">
        <div className="section-heading">
          <div>
            <p className="eyebrow">A simple way to meet</p>
            <h2 id="home-start-heading">Good things happen when you show up.</h2>
          </div>
          <Link className="text-link" to="/events">View all events</Link>
        </div>
        <div className="starting-grid">
          <article className="starting-item">
            <span className="item-number">01</span>
            <h3>Find your thing</h3>
            <p>Browse events by interest, from casual meetups to hands-on workshops.</p>
          </article>
          <article className="starting-item">
            <span className="item-number">02</span>
            <h3>Save your place</h3>
            <p>RSVP to keep track of the events you’re planning to attend.</p>
          </article>
          <article className="starting-item">
            <span className="item-number">03</span>
            <h3>Bring someone along</h3>
            <p>Share an event with a friend and make a plan together.</p>
          </article>
        </div>
      </section>
    </div>
  )
}

export default HomePage