import { useEffect, useState } from "react"
import { ApiError } from "../api/client"
import { getEvent } from "../api/events"
import type { EventDetail } from "../../types/event"

export function useEvent(eventId: number | null) {
  const [event, setEvent] = useState<EventDetail | null>(null)
  const [isLoading, setIsLoading] = useState(eventId !== null)
  const [error, setError] = useState<string | null>(null)
  const [errorStatus, setErrorStatus] = useState<number | null>(null)
  const [reloadCount, setReloadCount] = useState(0)

  useEffect(() => {
    let active = true

    if (eventId === null) {
      setEvent(null)
      setError(null)
      setErrorStatus(null)
      setIsLoading(false)
      return () => {
        active = false
      }
    }

    const requestedEventId = eventId

    async function loadEvent() {
      setIsLoading(true)
      setError(null)
      setErrorStatus(null)

      try {
        const result = await getEvent(requestedEventId)
        if (active) setEvent(result)
      } catch (cause: unknown) {
        if (active) {
          setEvent(null)
          setError(cause instanceof Error ? cause.message : "Could not load this event.")
          setErrorStatus(cause instanceof ApiError ? cause.status : null)
        }
      } finally {
        if (active) setIsLoading(false)
      }
    }

    void loadEvent()

    return () => {
      active = false
    }
  }, [eventId, reloadCount])

  function retry() {
    setReloadCount((count) => count + 1)
  }

  return { event, isLoading, error, errorStatus, retry }
}