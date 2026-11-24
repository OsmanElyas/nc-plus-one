const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

export async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed (${response.status})`);
  }
  return (await response.json()) as T;
}