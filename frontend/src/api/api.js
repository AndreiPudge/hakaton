// Базовый URL бэкенда (FastAPI/Flask и т.п.)
const API_BASE_URL =
process.env.REACT_APP_API_BASE_URL || "http://localhost:9000";

// Общая функция для запросов
async function apiRequest(path, options = {}) {
  const url =   `${API_BASE_URL}${path}`;

  const defaultHeaders = {
    "Content-Type": "application/json",
  };

  const response = await fetch(url, {
    headers: {
      ...defaultHeaders,
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    // Пытаемся вытащить текст ошибки с бэка
    let errorMessage = `API error: ${response.status} ${response.statusText}`;
    try {
      const errorData = await response.json();
      if (errorData && errorData.detail) {
        errorMessage = errorData.detail;
      }
    } catch (e) {
      // ignore JSON parse error
    }
    throw new Error(errorMessage);
  }

  // Если тело пустое — вернём null
  const text = await response.text();
  if (!text) return null;

  try {
    return JSON.parse(text);
  } catch (e) {
    // на всякий случай, если бэк вернул не JSON
    return text;
  }
}

// -------------------- КЛИЕНТЫ --------------------

// Получить список клиентов по поиску
// GET /api/clients?search=...
export async function fetchClientsApi(searchQuery) {
  const query = searchQuery ? searchQuery.trim() : "";
  const path = `/api/clients?search=${encodeURIComponent(query)}`;
  return apiRequest(path, {
    method: "GET",
  });
}

// -------------------- ИНСАЙТЫ ПО КЛИЕНТУ --------------------

// Получить прогноз дохода, факторы и рекомендации
// GET /api/clients/:id/insights
export async function fetchClientInsightsApi(clientId) {
  const path = `/api/clients/${clientId}/insights`;
  return apiRequest(path, {
    method: "GET",
  });
}