import { useEffect, useState } from "react";
import { listMyEvents } from "../api/rsvps";
import { useAuth } from "../auth/AuthProvider";
import type { MyEvent } from "../types/rsvp";

export function useMyEvents() {
  const { user, isLoading: isAuthLoading } = useAuth();
  const [events, setEvents] = useState<MyEvent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reloadCount, setReloadCount] = useState(0);

  useEffect(() => {
    let active = true;

    if (isAuthLoading) {
      setIsLoading(true);
      return () => {
        active = false;
      };
    }

    if (!user) {
      setEvents([]);
      setError(null);
      setIsLoading(false);
      return () => {
        active = false;
      };
    }

    async function loadEvents() {
      setIsLoading(true);
      setError(null);

      try {
        const result = await listMyEvents();
        if (active) setEvents(result);
      } catch (cause: unknown) {
        if (active) {
          setError(cause instanceof Error ? cause.message : "Could not load your events.");
        }
      } finally {
        if (active) setIsLoading(false);
      }
    }

    void loadEvents();

    return () => {
      active = false;
    };
  }, [isAuthLoading, reloadCount, user]);

  function refresh() {
    setReloadCount((count) => count + 1);
  }

  return { events, isLoading, error, refresh };
}