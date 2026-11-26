export interface AuthUser {
  id: number
  name: string
  email: string
  created_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterDetails extends LoginCredentials {
  name: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}