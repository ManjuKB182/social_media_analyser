from datetime import date, datetime
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fetchers import TwitterFetcher
from data_processor import process_data
from ai_agent import GeminiAgent


TopicKey = Literal["travel", "politics", "sports", "cinema"]
ModeKey = Literal["historical", "realtime"]


class DashboardFilters(BaseModel):
  topic: TopicKey
  fromDate: date
  toDate: date
  startHour: int = 0
  endHour: int = 23
  mode: ModeKey = "historical"


class MetricsHealth(BaseModel):
  total_records: str
  engagement: str
  timerange: str


class DashboardSummary(BaseModel):
  llmInsights: Optional[str]
  metricsHealth: Optional[MetricsHealth]


class DashboardResponse(BaseModel):
  topic: TopicKey
  filters: DashboardFilters
  summary: DashboardSummary
  rows: list[dict]


class AiInsightsRequest(BaseModel):
  topic: TopicKey
  fromDate: date
  toDate: date
  startHour: int = 0
  endHour: int = 23
  mode: ModeKey = "historical"


class AiInsightsResponse(BaseModel):
  topic: TopicKey
  filters: DashboardFilters
  insights: str
  llmProvider: Optional[str]
  fallback: bool


class AiChatRequest(BaseModel):
  topic: TopicKey
  question: str
  fromDate: date
  toDate: date
  startHour: int = 0
  endHour: int = 23
  mode: ModeKey = "historical"


class AiChatResponse(BaseModel):
  topic: TopicKey
  question: str
  answer: str
  llmProvider: Optional[str]
  fallback: bool


app = FastAPI(title="Social Media Analyser API", version="1.0.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


def _load_dataframe(filters: DashboardFilters):
  twitter = TwitterFetcher()

  if filters.mode == "realtime":
    trending_queries = []
    if filters.topic == "travel":
      trending_queries = [{"topic": "travel", "query": "travel India"}]
    elif filters.topic == "cinema":
      trending_queries = [{"topic": "cinema", "query": "cinema India"}]
    elif filters.topic == "politics":
      trending_queries = [{"topic": "politics", "query": "Karnataka politics"}]
    else:
      trending_queries = [{"topic": "sports", "query": "India sports"}]

    raw_tweets = twitter.fetch_realtime_trends(
      trending_queries, time_window_hrs=1, max_results_per_query=40
    )
    proc_topic = (
      "travel"
      if filters.topic == "travel"
      else "cinema"
      if filters.topic == "cinema"
      else "politics"
      if filters.topic == "politics"
      else "sports"
    )
    df = process_data(raw_tweets, topic=proc_topic)
  else:
    from_dt = filters.fromDate
    to_dt = filters.toDate

    if filters.topic == "travel":
      raw_tweets = twitter.fetch_trends(
        query="travel India", topic="travel", from_date=from_dt, end_date=to_dt
      )
      df = process_data(raw_tweets, topic="travel")
    elif filters.topic == "cinema":
      raw_tweets = twitter.fetch_trends(
        query="cinema India", topic="cinema", from_date=from_dt, end_date=to_dt
      )
      df = process_data(raw_tweets, topic="cinema")
    elif filters.topic == "politics":
      raw_tweets = twitter.fetch_politics_trends(
        from_date=from_dt, end_date=to_dt
      )
      df = process_data(raw_tweets, topic="politics")
    else:
      raw_tweets = twitter.fetch_sports_trends(
        from_date=from_dt, end_date=to_dt
      )
      df = process_data(raw_tweets, topic="sports")

  if df is not None and not df.empty:
    df = df[
      (df["Hour"] >= filters.startHour) & (df["Hour"] <= filters.endHour)
    ]

  TARGET_SAMPLE_SIZE = 100_000
  if df is not None and not df.empty:
    n = len(df)
    if n > TARGET_SAMPLE_SIZE:
      df = df.sample(n=TARGET_SAMPLE_SIZE, random_state=42)
    elif n < TARGET_SAMPLE_SIZE:
      df = df.sample(n=TARGET_SAMPLE_SIZE, replace=True, random_state=42)

  return df


@app.get("/health")
def health():
  return {
    "status": "ok",
    "service": "social-media-analyser-api",
    "version": "1.0.0",
  }


@app.get("/api/dashboard", response_model=DashboardResponse)
def get_dashboard(
  topic: TopicKey = Query(...),
  fromDate: date = Query(...),
  toDate: date = Query(...),
  startHour: int = Query(0, ge=0, le=23),
  endHour: int = Query(23, ge=0, le=23),
  mode: ModeKey = Query("historical"),
):
  if endHour < startHour:
    raise HTTPException(status_code=400, detail="endHour must be >= startHour")

  filters = DashboardFilters(
    topic=topic,
    fromDate=fromDate,
    toDate=toDate,
    startHour=startHour,
    endHour=endHour,
    mode=mode,
  )

  df = _load_dataframe(filters)
  agent = GeminiAgent()

  llm_insights = None
  metrics_health = None

  if df is not None and not df.empty:
    try:
      llm_insights = agent.generate_insights(df, topic.capitalize())
    except Exception as exc:
      llm_insights = f"Error generating insights: {exc}"

    try:
      metrics = agent.metric_health_summary(df, topic)
      metrics_health = MetricsHealth(**metrics)
    except Exception:
      metrics_health = None

  rows: list[dict] = []
  if df is not None and not df.empty:
    rows = df.to_dict(orient="records")

  summary = DashboardSummary(
    llmInsights=llm_insights,
    metricsHealth=metrics_health,
  )

  return DashboardResponse(
    topic=topic,
    filters=filters,
    summary=summary,
    rows=rows,
  )


@app.post("/api/ai/insights", response_model=AiInsightsResponse)
def ai_insights(payload: AiInsightsRequest):
  filters = DashboardFilters(
    topic=payload.topic,
    fromDate=payload.fromDate,
    toDate=payload.toDate,
    startHour=payload.startHour,
    endHour=payload.endHour,
    mode=payload.mode,
  )
  df = _load_dataframe(filters)
  agent = GeminiAgent()

  if df is None or df.empty:
    return AiInsightsResponse(
      topic=payload.topic,
      filters=filters,
      insights="No data available for analysis.",
      llmProvider=None,
      fallback=True,
    )

  fallback = False
  provider = None
  text = ""

  try:
    text = agent.generate_insights(df, payload.topic.capitalize())
    provider = "gemini-2.0-flash-exp"
  except Exception as exc:
    fallback = True
    text = f"Error generating insights: {exc}"

  return AiInsightsResponse(
    topic=payload.topic,
    filters=filters,
    insights=text,
    llmProvider=provider,
    fallback=fallback,
  )


@app.post("/api/ai/chat", response_model=AiChatResponse)
def ai_chat(payload: AiChatRequest):
  filters = DashboardFilters(
    topic=payload.topic,
    fromDate=payload.fromDate,
    toDate=payload.toDate,
    startHour=payload.startHour,
    endHour=payload.endHour,
    mode=payload.mode,
  )
  df = _load_dataframe(filters)
  agent = GeminiAgent()

  if df is None or df.empty:
    return AiChatResponse(
      topic=payload.topic,
      question=payload.question,
      answer="No data available for this window.",
      llmProvider=None,
      fallback=True,
    )

  fallback = False
  provider = None
  text = ""

  try:
    text = agent.chat_with_data(payload.question, df, payload.topic.capitalize())
    provider = "gemini-2.0-flash-exp"
  except Exception as exc:
    fallback = True
    text = f"Error processing chat: {exc}"

  return AiChatResponse(
    topic=payload.topic,
    question=payload.question,
    answer=text,
    llmProvider=provider,
    fallback=fallback,
  )


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)


