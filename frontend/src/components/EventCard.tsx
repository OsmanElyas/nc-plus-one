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
    const dateOptions: Intl.DateTimeFormatOptions = {
        weekday: "short",
        day: "numeric",
        month: "long",
        year: "numeric",
    }

    if (!isDateOnly) {
        dateOptions.hour = "2-digit"
        dateOptions.minute = "2-digit"
    }

    const formattedDate = dateIsValid
        ? new Intl.DateTimeFormat("en-GB", dateOptions).format(date)
        : event.starts_at

    return (
        <li className="event-card">
            <Link className="event-card__link" to={`/events/${event.id}`}>
                <time className="event-card__date" dateTime={event.starts_at}>
                    <span className="event-card__month">{month}</span>
                    <span className="event-card__day">{day}</span>
                </time>
                <div className="event-card__body">
                    <p className="event-card__eyebrow">EVENT {event.id}</p>
                    <h2 className="event-card__title">{event.title}</h2>
                    <p className="event-card__location">{event.location}</p>
                </div>
                <div className="event-card__footer">
                    <span className="event-card__full-date">{formattedDate}</span>
                    <span className="event-card__action">View details <span aria-hidden="true">&rarr;</span></span>
                </div>
            </Link>
        </li>
    )
}


export default EventCard
