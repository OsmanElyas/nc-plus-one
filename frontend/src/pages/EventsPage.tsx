import EventGrid from "../components/EventGrid"
import { useEvents } from "../hooks/useEvents"

function EventsPage() {
	const { events, isLoading, error } = useEvents()

	return (
		<section className="events-page">
			<header className="events-page__header">
				<div>
					<p className="events-page__eyebrow">Discover</p>
					  <h1 className="events-page__title">Explore events</h1>
					<p className="events-page__description">
						Find something happening near you and meet a few new people.
					</p>
				</div>
				{!isLoading && !error && (
					<p className="events-page__count">
						{events.length} {events.length === 1 ? "event" : "events"}
					</p>
				)}
			</header>

			{isLoading ? (
				<p className="events-page__message">Loading events...</p>
			) : error ? (
				<p className="events-page__message" role="alert">
					Couldn’t load events: {error}
				</p>
			) : events.length === 0 ? (
				<p className="events-page__message">No events are scheduled yet.</p>
			) : (
				<EventGrid events={events} />
			)}
		</section>
	)
}

export default EventsPage
