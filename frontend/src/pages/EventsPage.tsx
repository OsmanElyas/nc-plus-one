import { Link } from "react-router"
import EventGrid from "../components/EventGrid"
import { useEvents } from "../hooks/useEvents";
import NotFoundPage from "./NotFoundPage";

function EventsPage() {
    const { events, isLoading, error } = useEvents();
    if (isLoading) return <p>Loading events...</p>

    if (error) {
        return <NotFoundPage/>
    }

    if (events.length === 0) return <p>No events are scheduled yet.</p>;

	return (
		<section className="placeholder-page">
			<p className="eyebrow">Discover</p>
			<h1>Events</h1>
            <EventGrid events={events}/>
			<Link className="text-link" to="/">
				Back to home
			</Link>
		</section>
	)
}

export default EventsPage
