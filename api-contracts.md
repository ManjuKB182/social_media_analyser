## API Contracts – Social Media Analyser

This document defines the HTTP API boundary between the **Next.js frontend** and the **Python backend**.

The initial backend is the existing Python codebase (Twitter fetching, mock generators, data processing, Gemini AI). Responses are JSON and stable so that storage can later move to MongoDB or a Node/Next.js API layer without breaking the React UI.

---

### 1. Health

**Endpoint**

- `GET /health`

**Response 200**

```json
{
  "status": "ok",
  "service": "social-media-analyser-api",
  "version": "1.0.0"
}
```

---

### 2. Dashboard data (core topic analytics)

Unified endpoint for the 4 dashboard topics currently handled in `app.py`:

- Travel
- Politics
- Sports
- Cinema

**Endpoint**

- `GET /api/dashboard`

**Query parameters**

- `topic` (string; required)
  - One of: `"travel" | "politics" | "sports" | "cinema"`
- `fromDate` (string; required)
  - ISO date `YYYY-MM-DD`
- `toDate` (string; required)
  - ISO date `YYYY-MM-DD`
- `startHour` (integer; optional, default `0`)
  - 0–23 inclusive
- `endHour` (integer; optional, default `23`)
  - 0–23 inclusive; must be `>= startHour`
- `mode` (string; optional, default `"historical"`)
  - `"historical"` – uses the same logic as `load_data(...)` in `app.py`
  - `"realtime"` – uses the same logic as the `fetch_latest` branch in `app.py` (last N hours with `fetch_realtime_trends`)

**Base response shape**

```json
{
  "topic": "travel",
  "filters": {
    "fromDate": "2025-01-01",
    "toDate": "2025-01-02",
    "startHour": 0,
    "endHour": 23,
    "mode": "historical"
  },
  "summary": {
    "llmInsights": "string (Gemini-generated summary or fallback message)",
    "metricsHealth": {
      "total_records": "string label (e.g. '🟢 High volume')",
      "engagement": "string label",
      "timerange": "string label"
    }
  },
  "rows": [
    {
      "...": "see per-topic row shapes below"
    }
  ]
}
```

The `rows` field corresponds to the processed DataFrame produced by `process_data(...)` for each topic (`df.to_dict(orient="records")`).

#### 2.1 Travel dashboard rows

Produced by `process_data(..., topic="travel")`.

**Row shape**

```json
{
  "Location": "Goa",
  "State": "Goa",
  "Category": "Beach",
  "Text": "string – tweet text",
  "Likes": 123,
  "Retweets": 45,
  "Engagement": 168,
  "Hour": 14,
  "Sentiment": 0.0,
  "Sex": "M",
  "AgeGroup": "25-34",
  "UserLocationRaw": "Goa, India"
}
```

#### 2.2 Politics dashboard rows

Produced by `process_data(..., topic="politics")`.

**Row shape**

```json
{
  "Party": "Congress",
  "Politician": "Siddaramaiah",
  "Location": "Bangalore",
  "State": "Karnataka",
  "Text": "string – tweet text",
  "Likes": 123,
  "Retweets": 45,
  "Engagement": 168,
  "Hour": 14,
  "Sentiment": 0.0,
  "Sex": "M",
  "AgeGroup": "25-34",
  "UserLocationRaw": "Bangalore, India"
}
```

#### 2.3 Sports dashboard rows

Produced by `process_data(..., topic="sports")`.

**Row shape**

```json
{
  "Sport": "Cricket",
  "Location": "Mumbai",
  "State": "Maharashtra",
  "Text": "string – tweet text",
  "Likes": 123,
  "Retweets": 45,
  "Engagement": 168,
  "Hour": 18,
  "Sentiment": 0.0,
  "Sex": "F",
  "AgeGroup": "18-24",
  "UserLocationRaw": "Mumbai, India"
}
```

#### 2.4 Cinema dashboard rows

Produced by `process_data(..., topic="cinema")`.

**Row shape**

```json
{
  "Movie": "KGF 3",
  "Industry": "Sandalwood",
  "Location": "Bangalore",
  "State": "Karnataka",
  "Text": "string – tweet text",
  "Likes": 321,
  "Retweets": 80,
  "Engagement": 401,
  "Hour": 21,
  "Sentiment": 0.0,
  "Sex": "M",
  "AgeGroup": "25-34",
  "UserLocationRaw": "Bangalore, India"
}
```

---

### 3. AI insights over dashboard data

High-level AI commentary over the same dashboard filters, powered by `GeminiAgent`.

**Endpoint**

- `POST /api/ai/insights`

**Request body**

```json
{
  "topic": "travel",
  "fromDate": "2025-01-01",
  "toDate": "2025-01-02",
  "startHour": 0,
  "endHour": 23,
  "mode": "historical"
}
```

Semantics match `/api/dashboard` filters; the backend internally rebuilds the DataFrame and calls `GeminiAgent.generate_insights(...)`.

**Response 200**

```json
{
  "topic": "travel",
  "filters": {
    "fromDate": "2025-01-01",
    "toDate": "2025-01-02",
    "startHour": 0,
    "endHour": 23,
    "mode": "historical"
  },
  "insights": "★ Bullet-point Gemini insights...\n★ Another point...",
  "llmProvider": "gemini-2.0-flash-exp",
  "fallback": false
}
```

When `GEMINI_API_KEY` is not configured or the call fails, `fallback` is `true` and `insights` contains a human-readable error or rule-based summary.

---

### 4. AI chat with data

Chat-style interaction over the same data window, powered by `GeminiAgent.chat_with_data`.

**Endpoint**

- `POST /api/ai/chat`

**Request body**

```json
{
  "topic": "travel",
  "question": "Which cities are driving the most engagement tonight?",
  "fromDate": "2025-01-01",
  "toDate": "2025-01-02",
  "startHour": 18,
  "endHour": 23,
  "mode": "realtime"
}
```

**Response 200**

```json
{
  "topic": "travel",
  "question": "Which cities are driving the most engagement tonight?",
  "answer": "string – Gemini answer grounded in the current data window",
  "llmProvider": "gemini-2.0-flash-exp",
  "fallback": false
}
```

If chat is unavailable (no API key or error), `fallback` is `true` and `answer` is a message explaining that AI chat is disabled.

---

### 5. Future MongoDB-backed extensions (non-breaking)

These contracts are intentionally **storage-agnostic**:

- The frontend always speaks in terms of **topics**, **filters**, and **rows** as defined above.
- The backend is free to:
  - Read from live APIs (Twitter etc.)
  - Read/write cached/aggregated data in MongoDB
  - Combine both (e.g., cold data from DB + hot data from APIs)

Future extensions can add endpoints such as:

- `GET /api/dashboard/cache-status`
- `POST /api/dashboard/recompute`

…as long as the existing endpoints and response shapes remain backward-compatible for the Next.js UI.


