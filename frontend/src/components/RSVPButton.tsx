import { useEffect, useRef, useState } from "react"
import { Link } from "react-router"
import { useAuth } from "../auth/AuthProvider"
import { addRSVP, cancelRSVP } from "../api/rsvps"

interface RSVPButtonProps {
    eventId: number
    isRsvped: boolean
    isLoading?: boolean
    onChanged?: () => void | Promise<void>
}

function RSVPButton({ eventId, isRsvped, isLoading = false, onChanged }: RSVPButtonProps) {
    const { user, isLoading: isAuthLoading } = useAuth()
    const [hasRsvped, setHasRsvped] = useState(isRsvped)
    const [pendingAction, setPendingAction] = useState<"rsvp" | "cancel" | null>(null)
    const [error, setError] = useState<string | null>(null)
    const requestInFlight = useRef(false)

    useEffect(() => {
        setHasRsvped(isRsvped)
    }, [eventId, isRsvped])

    async function handleClick() {
        if (requestInFlight.current || isLoading) return

        requestInFlight.current = true
        const action = hasRsvped ? "cancel" : "rsvp"
        setPendingAction(action)
        setError(null)

        try {
            if (action === "cancel") {
                await cancelRSVP(eventId)
            } else {
                await addRSVP(eventId)
            }

            setHasRsvped(action === "rsvp")
            await onChanged?.()
        } catch (cause: unknown) {
            setError(cause instanceof Error ? cause.message : "Could not update your RSVP.")
        } finally {
            requestInFlight.current = false
            setPendingAction(null)
        }
    }

    if (isAuthLoading) {
        return <button className="rsvp-action" type="button" disabled>Checking account...</button>
    }

    if (!user) {
        return <Link className="rsvp-signin" to="/login">Sign in to RSVP</Link>
    }

    const isDisabled = isLoading || pendingAction !== null
    const buttonLabel = pendingAction === "rsvp"
        ? "Saving RSVP..."
        : pendingAction === "cancel"
            ? "Cancelling..."
            : isLoading
                ? "Checking RSVP..."
                : hasRsvped
                    ? "RSVPed"
                    : "RSVP"

    return (
        <div className="rsvp-control">
            <button
                className={`rsvp-action${hasRsvped ? " rsvp-action--done" : ""}`}
                type="button"
                aria-pressed={hasRsvped}
                aria-label={hasRsvped ? "Cancel your RSVP" : "RSVP to this event"}
                disabled={isDisabled}
                onClick={handleClick}
            >
                {buttonLabel}
            </button>
            {error && <p className="rsvp-error" role="alert">{error}</p>}
        </div>
    )
}

export default RSVPButton