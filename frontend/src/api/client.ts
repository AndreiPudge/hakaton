
const API_BASE_URL = "http://localhost:9000"; 
// пусто → используется proxy / same-origin

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

async function request<T>(
  url: string,
  method: HttpMethod,
  body?: unknown
): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method,
      headers: {
        "Content-Type": "application/json",
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    // backend ответил, но с ошибкой
    if (!response.ok) {
      if (response.status >= 500) {
        throw new Error("SERVER_ERROR");
      }
      throw new Error("REQUEST_ERROR");
    }

    return (await response.json()) as T;
  } catch (error) {
    // backend недоступен / упал / нет сети
    if (error instanceof TypeError) {
      throw new Error("NETWORK_ERROR");
    }
    throw error;
  }
}

export const httpClient = {
  get: <T>(url: string) => request<T>(url, "GET"),
  post: <T>(url: string, body?: unknown) => request<T>(url, "POST", body),
  put: <T>(url: string, body?: unknown) => request<T>(url, "PUT", body),
  patch: <T>(url: string, body?: unknown) => request<T>(url, "PATCH", body),
  delete: <T>(url: string) => request<T>(url, "DELETE"),
};
