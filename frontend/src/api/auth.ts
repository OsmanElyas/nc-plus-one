import { getJson, postJson } from "./client"
import type { AuthUser, LoginCredentials, LoginResponse, RegisterDetails } from "../types/auth"

export function login(credentials: LoginCredentials): Promise<LoginResponse> {
  return postJson<LoginCredentials, LoginResponse>("/api/auth/login", credentials)
}

export async function register(details: RegisterDetails): Promise<AuthUser> {
  const response = await postJson<RegisterDetails, { user: AuthUser }>("/api/auth/register", details)
  return response.user
}

export async function getCurrentUser(): Promise<AuthUser> {
  const response = await getJson<{ user: AuthUser }>("/api/user/me")
  return response.user
}