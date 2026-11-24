import { getJson } from "./client";
import type { Event } from "../../types/event";

export async function listEvents(): Promise<Event[]> {
  const result = await getJson<{ events: Event[] }>("/api/events");
  return result.events;
}