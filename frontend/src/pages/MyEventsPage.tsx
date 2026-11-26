import { Link } from "react-router";
import { useMyEvents } from "../hooks/useMyEvents";

function formatDate(value: string) {
  const dateOnly = /^\d{4}-\d{2}-\d{2}$/.test(value);
  const date = new Date(dateOnly ? `${value}T12:00:00` : value);

  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    ...(dateOnly ? {} : { timeStyle: "short" }),
  }).format(date);
}

function MyEventsPage() {
  const { events, isLoading, error, refresh } = useMyEvents();

  return (
    <section className="my-events-page">
      <header className="my-events-header">
        <div>
          <p className="my-events-eyebrow">Your plans</p>
          <h1 className="my-events-title">My events</h1>
          <p className="my-events-description">Events you’ve saved a place for.</p>
        </div>
        {!isLoading && !error && events.length > 0 && (
          <p className="my-events-count">
            <strong>{events.length}</strong>
            <span>{events.length === 1 ? "event" : "events"}</span>
          </p>
        )}
      </header>

      {isLoading ? (
        <p className="my-events-state" role="status">Loading your events...</p>
      ) : error ? (
        <div className="my-events-state my-events-state--error" role="alert">
          <p>Couldn’t load your events: {error}</p>
          <button className="my-events-retry" type="button" onClick={refresh}>Try again</button>
        </div>
      ) : events.length === 0 ? (
        <div className="my-events-state my-events-state--empty">
          <h2>No RSVPs yet</h2>
          <p>When you RSVP to an event, it’ll be listed here.</p>
          <Link className="my-events-explore" to="/events">Explore events <span aria-hidden="true">&rarr;</span></Link>
        </div>
      ) : (
        <div className="my-events-list">
          <div className="my-events-list__head" aria-hidden="true">
            <span>Event</span>
            <span>Date</span>
            <span>Your list</span>
          </div>
          <ol className="my-events-list__rows">
            {events.map((event) => (
              <li key={event.id}>
                <Link className="my-event-row" to={`/events/${event.id}`}>
                <div className="my-event-row__name">
                  <h2>{event.title}</h2>
                </div>
                <time className="my-event-row__date" dateTime={event.starts_at}>
                  {formatDate(event.starts_at)}
                </time>
                <p className="my-event-row__rank">
                  <strong>{event.event_rank}</strong>
                  <span>of {event.total_rsvps}</span>
                </p>
                </Link>
              </li>
            ))}
          </ol>
        </div>
      )}
    </section>
  );
}

export default MyEventsPage;