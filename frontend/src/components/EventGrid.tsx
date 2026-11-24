import EventCard from "./EventCard";
import type { Event } from "../../types/event";

interface EventGridProps {
    events: Event[];
}

function EventGrid(props: EventGridProps) {

    const {events} = props

    return (
        <ul className="event-grid">
            {events.map((event) => (
                <EventCard key={event.id} event={event} />
            ))}
        </ul>
    );
}

export default EventGrid