import { API_BASE_URL } from "./config";
import type {
  AiChatRequest,
  AiChatResponse,
  AiInsightsRequest,
  AiInsightsResponse,
  DashboardFilters,
  DashboardResponse,
  TopicKey
} from "./types";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API error ${res.status}: ${text || res.statusText}`);
  }
  return (await res.json()) as T;
}

export async function getDashboard<T extends TopicKey>(
  filters: DashboardFilters & { topic: T }
): Promise<DashboardResponse<T>> {
  const params = new URLSearchParams({
    topic: filters.topic,
    fromDate: filters.fromDate,
    toDate: filters.toDate,
    startHour: String(filters.startHour),
    endHour: String(filters.endHour),
    mode: filters.mode ?? "historical"
  });

  const res = await fetch(`${API_BASE_URL}/api/dashboard?${params.toString()}`, {
    next: { revalidate: 0 }
  });

  return handleResponse<DashboardResponse<T>>(res);
}

export async function getAiInsights(
  payload: AiInsightsRequest
): Promise<AiInsightsResponse> {
  const res = await fetch(`${API_BASE_URL}/api/ai/insights`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return handleResponse<AiInsightsResponse>(res);
}

export async function postAiChat(
  payload: AiChatRequest
): Promise<AiChatResponse> {
  const res = await fetch(`${API_BASE_URL}/api/ai/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return handleResponse<AiChatResponse>(res);
}


