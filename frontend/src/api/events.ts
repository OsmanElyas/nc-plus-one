import { getJson } from "./client";
import type { Event, EventDetail } from "../../types/event";

export async function listEvents(): Promise<Event[]> {
  const result = await getJson<{ events: Event[] }>("/api/events");
  return result.events;
}

export function getEvent(eventId: number): Promise<EventDetail> {
  return getJson<EventDetail>(`/api/events/${eventId}`)
}