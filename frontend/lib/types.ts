export type TopicKey = "travel" | "politics" | "sports" | "cinema";

export interface DashboardFilters {
  topic: TopicKey;
  fromDate: string; // YYYY-MM-DD
  toDate: string; // YYYY-MM-DD
  startHour: number;
  endHour: number;
  mode?: "historical" | "realtime";
}

export interface MetricsHealth {
  total_records: string;
  engagement: string;
  timerange: string;
}

export interface DashboardSummary {
  llmInsights: string | null;
  metricsHealth: MetricsHealth | null;
}

export interface TravelRow {
  Location: string;
  State: string;
  Category: string;
  Text: string;
  Likes: number;
  Retweets: number;
  Engagement: number;
  Hour: number;
  Sentiment: number;
  Sex: string;
  AgeGroup: string;
  UserLocationRaw: string;
}

export interface PoliticsRow {
  Party: string;
  Politician: string;
  Location: string;
  State: string;
  Text: string;
  Likes: number;
  Retweets: number;
  Engagement: number;
  Hour: number;
  Sentiment: number;
  Sex: string;
  AgeGroup: string;
  UserLocationRaw: string;
}

export interface SportsRow {
  Sport: string;
  Location: string;
  State: string;
  Text: string;
  Likes: number;
  Retweets: number;
  Engagement: number;
  Hour: number;
  Sentiment: number;
  Sex: string;
  AgeGroup: string;
  UserLocationRaw: string;
}

export interface CinemaRow {
  Movie: string;
  Industry: string;
  Location: string;
  State: string;
  Text: string;
  Likes: number;
  Retweets: number;
  Engagement: number;
  Hour: number;
  Sentiment: number;
  Sex: string;
  AgeGroup: string;
  UserLocationRaw: string;
}

export type RowByTopic<T extends TopicKey> = T extends "travel"
  ? TravelRow
  : T extends "politics"
  ? PoliticsRow
  : T extends "sports"
  ? SportsRow
  : CinemaRow;

export interface DashboardResponse<T extends TopicKey> {
  topic: T;
  filters: DashboardFilters;
  summary: DashboardSummary;
  rows: RowByTopic<T>[];
}

export interface AiInsightsRequest {
  topic: TopicKey;
  fromDate: string;
  toDate: string;
  startHour: number;
  endHour: number;
  mode?: "historical" | "realtime";
}

export interface AiInsightsResponse {
  topic: TopicKey;
  filters: DashboardFilters;
  insights: string;
  llmProvider: string | null;
  fallback: boolean;
}

export interface AiChatRequest {
  topic: TopicKey;
  question: string;
  fromDate: string;
  toDate: string;
  startHour: number;
  endHour: number;
  mode?: "historical" | "realtime";
}

export interface AiChatResponse {
  topic: TopicKey;
  question: string;
  answer: string;
  llmProvider: string | null;
  fallback: boolean;
}


