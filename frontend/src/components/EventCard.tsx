import { Link } from "react-router"
import type { Event } from "../../types/event"

interface EventCardProps {
    event: Event
}


function EventCard({ event }: EventCardProps) {
    const isDateOnly = /^\d{4}-\d{2}-\d{2}$/.test(event.starts_at)
    const date = new Date(isDateOnly ? `${event.starts_at}T12:00:00` : event.starts_at)
    const dateIsValid = !Number.isNaN(date.getTime())
    const month = dateIsValid
        ? new Intl.DateTimeFormat("en-GB", { month: "short" }).format(date)
        : "DATE"
    const day = dateIsValid
        ? new Intl.DateTimeFormat("en-GB", { day: "2-digit" }).format(date)
        : "--"
    const year = dateIsValid
        ? new Intl.DateTimeFormat("en-GB", { year: "numeric" }).format(date)
        : "----"
    const startTime = dateIsValid && !isDateOnly
        ? new Intl.DateTimeFormat("en-GB", { hour: "numeric", minute: "2-digit" }).format(date)
        : null

    return (
        <li className="event-card">
            <Link className="event-card__link" to={`/events/${event.id}`}>
                <time className="event-card__date" dateTime={event.starts_at}>
                    <span className="event-card__month">{month}</span>
                    <span className="event-card__day">{day}</span>
                    <span className="event-card__year">{year}</span>
                </time>
                <div className="event-card__body">
                    <h2 className="event-card__title">{event.title}</h2>
                    <p className="event-card__location">{event.location}</p>
                    {startTime && <p className="event-card__time">Starts at {startTime}</p>}
                </div>
                <div className="event-card__footer">
                    <span className="event-card__action">View details <span aria-hidden="true">&rarr;</span></span>
                </div>
            </Link>
        </li>
    )
}


export default EventCard
