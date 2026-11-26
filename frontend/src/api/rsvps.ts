import type { MyEvent } from "../types/rsvp";
import { requestJson } from "./client";


interface Rsvp {
  rsvp_id: number;
  attendee_id: number;
  event_id: number;
  created_at: string;
}

interface AddRsvpResponse {
  rsvp: Rsvp;
}



export async function addRSVP(eventId: number): Promise<AddRsvpResponse> {
  return requestJson<AddRsvpResponse>(`/api/events/${eventId}/rsvp`, {method: "POST"} );
}

export async function cancelRSVP(eventId: number): Promise<void> {
  await requestJson<null>(`/api/events/${eventId}/rsvp/me`, { method: "DELETE" });
}

export async function listMyEvents(): Promise<MyEvent[]> {
    const result = await requestJson<{ events: MyEvent[] }>("/api/user/me/events")
    return result.events
}