import { Link, useParams } from "react-router"
import RSVPButton from "../components/RSVPButton"
import { useMyEvents } from "../hooks/useMyEvents"
import { useEvent } from "../hooks/useEvent"

function formatEventDate(value: string) {
  const dateOnly = /^\d{4}-\d{2}-\d{2}$/.test(value)
  const date = new Date(dateOnly ? `${value}T12:00:00` : value)

  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "full",
    ...(dateOnly ? {} : { timeStyle: "short" }),
  }).format(date)
}

function EventDetailPage() {
  const { eventId: rawEventId } = useParams()
  const parsedEventId = Number(rawEventId)
  const hasValidId = Boolean(rawEventId && /^\d+$/.test(rawEventId) && Number.isSafeInteger(parsedEventId) && parsedEventId > 0)
  const { event, isLoading, error, errorStatus, retry } = useEvent(hasValidId ? parsedEventId : null)
  const {
    events: myEvents,
    isLoading: isMyEventsLoading,
    error: myEventsError,
    refresh: refreshMyEvents,
  } = useMyEvents()

  if (!hasValidId || errorStatus === 400 || errorStatus === 404) {
    return (
      <section className="event-detail-state">
        <p className="event-detail-eyebrow">Event not found</p>
        <h1>We couldn’t find that event.</h1>
        <p>Check the event link or go back to explore what’s on.</p>
        <Link className="button button-coral" to="/events">Explore events</Link>
      </section>
    )
  }

  if (isLoading) {
    return <p className="event-detail-state" role="status">Loading event details...</p>
  }

  if (error || !event) {
    return (
      <section className="event-detail-state">
        <p className="event-detail-eyebrow">Couldn’t load this event</p>
        <p role="alert">{error ?? "Please try again."}</p>
        <button className="event-detail-retry" type="button" onClick={retry}>Try again</button>
        <Link className="event-detail-back" to="/events">Back to events</Link>
      </section>
    )
  }

  return (
    <article className="event-detail-page">
      <Link className="event-detail-back" to="/events">&larr; All events</Link>

      <header className="event-detail-hero">
        <time className="event-detail-date" dateTime={event.starts_at}>
          <span>{new Intl.DateTimeFormat("en-GB", { month: "short" }).format(new Date(/^\d{4}-\d{2}-\d{2}$/.test(event.starts_at) ? `${event.starts_at}T12:00:00` : event.starts_at))}</span>
          <strong>{new Intl.DateTimeFormat("en-GB", { day: "2-digit" }).format(new Date(/^\d{4}-\d{2}-\d{2}$/.test(event.starts_at) ? `${event.starts_at}T12:00:00` : event.starts_at))}</strong>
        </time>
        <div className="event-detail-heading">
          <p className="event-detail-eyebrow">Event details</p>
          <h1>{event.title}</h1>
          <p>{event.location}</p>
        </div>
        <div className="event-detail-rsvp">
          <RSVPButton
            eventId={event.id}
            isRsvped={myEvents.some((myEvent) => myEvent.id === event.id)}
            isLoading={isMyEventsLoading || Boolean(myEventsError)}
            onChanged={refreshMyEvents}
          />
          {myEventsError && (
            <p className="event-detail-rsvp-error" role="alert">
              RSVP status unavailable. <button type="button" onClick={refreshMyEvents}>Retry</button>
            </p>
          )}
        </div>
      </header>

      <div className="event-detail-content">
        <section className="event-detail-about">
          <p className="event-detail-eyebrow">About this event</p>
          <p>{event.description || "More information about this event hasn’t been added yet."}</p>
        </section>

        <aside className="event-detail-facts" aria-labelledby="event-facts-title">
          <h2 id="event-facts-title">Event information</h2>
          <dl>
            <div>
              <dt>Starts</dt>
              <dd><time dateTime={event.starts_at}>{formatEventDate(event.starts_at)}</time></dd>
            </div>
            <div>
              <dt>Ends</dt>
              <dd><time dateTime={event.ends_at}>{formatEventDate(event.ends_at)}</time></dd>
            </div>
            <div>
              <dt>Venue</dt>
              <dd>{event.location}</dd>
            </div>
            <div>
              <dt>Address</dt>
              <dd>{event.address || "Address not provided"}</dd>
            </div>
            <div>
              <dt>Capacity</dt>
              <dd>{event.capacity === null ? "Not specified" : `${event.capacity} people`}</dd>
            </div>
          </dl>
          <div className="event-detail-organiser">
            <span className="event-detail-organiser__mark" aria-hidden="true">
              {event.organiser?.name.split(/\s+/).map((part) => part[0]).join("").slice(0, 2).toUpperCase() || "+1"}
            </span>
            <div>
              <p className="event-detail-organiser__label">Organised by</p>
              <p className="event-detail-organiser__name">
                {event.organiser?.name ?? "Community organiser"}
              </p>
            </div>
          </div>
        </aside>
      </div>
    </article>
  )
}

export default EventDetailPage