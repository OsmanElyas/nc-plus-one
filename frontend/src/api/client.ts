import { clearAccessToken, getAccessToken, AUTH_EXPIRED_EVENT } from "../auth/token"

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

async function readResponse(response: Response): Promise<unknown> {
  const text = await response.text()
  if (!text) return null

  try {
    return JSON.parse(text) as unknown
  } catch {
    return text
  }
}

function getErrorMessage(payload: unknown, status: number): string {
  if (typeof payload === "string") return payload

  if (payload && typeof payload === "object") {
    const body = payload as { error?: unknown; detail?: unknown }
    if (typeof body.error === "string") return body.error
    if (typeof body.detail === "string") return body.detail

    if (body.error && typeof body.error === "object" && "message" in body.error) {
      const message = body.error.message
      if (typeof message === "string") return message
    }

    if (body.detail && typeof body.detail === "object" && "message" in body.detail) {
      const message = body.detail.message
      if (typeof message === "string") return message
    }
  }

  return `Request failed (${status})`
}

export async function requestJson<T>(path: string, init: RequestInit = {}): Promise<T> {
  if (!apiBaseUrl) {
    throw new Error("VITE_API_BASE_URL is not configured")
  }

  const headers = new Headers(init.headers)
  if (init.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json")
  }

  const token = getAccessToken()
  if (token) headers.set("Authorization", `Bearer ${token}`)

  const response = await fetch(`${apiBaseUrl}${path}`, { ...init, headers })
  const payload = await readResponse(response)

  if (response.status === 401 && token) {
    clearAccessToken()
    window.dispatchEvent(new Event(AUTH_EXPIRED_EVENT))
  }

  if (!response.ok) {
    throw new ApiError(getErrorMessage(payload, response.status), response.status)
  }

  return payload as T
}

export function getJson<T>(path: string): Promise<T> {
  return requestJson<T>(path)
}

export function postJson<TBody, TResult>(path: string, body: TBody): Promise<TResult> {
  return requestJson<TResult>(path, {
    method: "POST",
    body: JSON.stringify(body),
  })
}