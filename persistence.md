## Persistence & MongoDB path

The current system is **stateless** from the perspective of this repo:

- Data is pulled live from Twitter (or generated as mock data) via `TwitterFetcher` / `TweetGenerator`.
- Analytics are computed in memory in `data_processor.process_data` and served via `api_server.py`.
- No DB writes are performed yet.

This document outlines how to move to MongoDB without changing the Next.js UI.

### 1. Abstraction point in Python

Introduce a small repository/service layer that hides where tweets and aggregates are stored:

- `repositories/tweets_repository.py`
  - `save_raw_tweets(topic, tweets, window_key)`
  - `load_raw_tweets(topic, from_date, to_date)`
  - `save_aggregate(topic, filters, df)`
  - `load_aggregate(topic, filters)`

`api_server._load_dataframe` should be the only place that calls into this repository. Initially it can be a pure in-memory/no-op implementation; later it can be wired to MongoDB.

### 2. MongoDB-backed implementation (future)

For a MongoDB deployment, a second implementation of the repository can:

- Use a `tweets` collection for raw tweet documents.
- Use an `aggregates` collection for pre-computed DataFrame-like documents keyed by:
  - `topic`
  - `fromDate`, `toDate`
  - `startHour`, `endHour`
  - `mode`

Internally:

- `save_raw_tweets` inserts/updates raw tweet documents.
- `load_raw_tweets` queries by `topic` and `created_at` range.
- `save_aggregate` stores the processed `df.to_dict(orient="records")` in an `aggregates` collection.
- `load_aggregate` can short-circuit `_load_dataframe` when a matching aggregate is found.

The FastAPI endpoints and the Next.js types/API client continue to use the same JSON shapes defined in `api-contracts.md`, so the frontend remains unchanged.


