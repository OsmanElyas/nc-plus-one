import EventCard from "./EventCard";
import type { Event } from "../../types/event";
import type { MyEvent } from "../types/rsvp";

interface EventGridProps {
    events: Event[];
    myEvents: MyEvent[];
    isRsvpLoading: boolean;
    onRsvpChanged: () => void;
}

function EventGrid(props: EventGridProps) {

    const {events, myEvents, isRsvpLoading, onRsvpChanged} = props

    return (
        <ul className="event-grid">
            {events.map((event) => (
                <EventCard
                    key={event.id}
                    event={event}
                    isRsvped={myEvents.some((myEvent) => myEvent.id === event.id)}
                    isRsvpLoading={isRsvpLoading}
                    onRsvpChanged={onRsvpChanged}
                />
            ))}
        </ul>
    );
}

export default EventGrid