import os
import requests
import tweepy
from datetime import datetime, timedelta
from tweet_generator import TweetGenerator

class TwitterFetcher:
    def __init__(self):
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        self.client = None
        if self.bearer_token and self.bearer_token.strip():
            try:
                self.client = tweepy.Client(bearer_token=self.bearer_token)
            except Exception as e:
                print(f"Error initializing Twitter client: {e}")
    
    def fetch_trends(self, query=None, topic=None, max_results=20, from_date=None, end_date=None):
        """
        Fetches recent tweets for a general topic/query,
        Returns a list of dicts with topic, text, metrics, and timestamp info.
        """
        if not query:
            query = "travel India"
        if not topic:
            topic = "general"
        if not self.client:
            print("Twitter client not initialized. Returning mock data.")
            return self._get_mock_data(topic, from_date, end_date)
        try:
            response = self.client.search_recent_tweets(
                query=f"{query} -is:retweet lang:en",
                max_results=max_results,
                tweet_fields=['created_at', 'geo', 'entities', 'public_metrics', 'text', 'author_id'],
                user_fields=['name', 'location', 'description'],
                expansions=['author_id'],
            )
            results = []
            # Build user lookup for demographics
            user_map = {}
            includes = getattr(response, "includes", None)
            if includes and "users" in includes:
                for u in includes["users"]:
                    user_map[getattr(u, "id", None)] = u

            if response.data:
                for tweet in response.data:
                    location = "Unknown"
                    if getattr(tweet, 'entities', None) and 'annotations' in tweet.entities:
                        for annotation in tweet.entities['annotations']:
                            if annotation['type'] == 'Place':
                                location = annotation['normalized_text']
                                break
                    metrics = tweet.public_metrics if hasattr(tweet, 'public_metrics') else {}
                    u = user_map.get(getattr(tweet, "author_id", None))
                    user_name = getattr(u, "name", None) if u else None
                    user_location_raw = getattr(u, "location", None) if u else None
                    # Very light heuristic: we don't have true sex; keep Unknown for real API
                    user_sex = None
                    # Age group is unknown for real data; can be filled later via enrichment
                    user_age_group = None
                    results.append({
                        "topic": topic,
                        "text": tweet.text,
                        "location": location,
                        "likes": metrics.get('like_count'),
                        "retweets": metrics.get('retweet_count'),
                        "replies": metrics.get('reply_count') if 'reply_count' in metrics else None,
                        "quotes": metrics.get('quote_count') if 'quote_count' in metrics else None,
                        "created_at": tweet.created_at,
                        "author_id": getattr(tweet, 'author_id', None),
                        "source": "api",
                        # user-level metadata (best-effort for real API)
                        "user_id": getattr(tweet, 'author_id', None),
                        "user_name": user_name,
                        "user_sex": user_sex,
                        "user_age_group": user_age_group,
                        "user_location_raw": user_location_raw or location,
                    })
            return results
        except Exception as e:
            print(f"Error fetching Twitter trends: {e}")
            return []

    def fetch_realtime_trends(self, trending_querylist, time_window_hrs=1, max_results_per_query=10):
        """
        For a list of trending queries (from LLM/topics), fetch most recent tweets for each, windowed to the specified past hours.
        Returns combined results with topic annotation.
        """
        now = datetime.utcnow()
        from_time = now - timedelta(hours=time_window_hrs)
        all_trends = []
        for topic_query in trending_querylist:
            topic = topic_query.get('topic') if isinstance(topic_query, dict) else 'general'
            query = topic_query.get('query') if isinstance(topic_query, dict) else topic_query
            try:
                data = self.fetch_trends(
                    query=query,
                    topic=topic,
                    max_results=max_results_per_query,
                    from_date=from_time,
                    end_date=now,
                )
                # Tag recency for velocity
                for d in data:
                    d['velocity_window_hours'] = time_window_hrs
                all_trends.extend(data)
            except Exception as e:
                print(f"Error fetching real-time trend for {query}: {e}")
        return all_trends
    
    # All topic-specific fetch_x_trends now call fetch_trends for DRY
    def fetch_politics_trends(self, **kwargs):
        return self.fetch_trends(query="Karnataka politics", topic="politics", **kwargs)
    
    def fetch_sports_trends(self, **kwargs):
        return self.fetch_trends(query="India sports", topic="sports", **kwargs)
    
    # --- MOCK data logic ---
    def _get_mock_data(self, topic, from_date=None, end_date=None):
        if topic == "politics":
            return TweetGenerator.generate_politics_tweets(count=100000, from_date=from_date, end_date=end_date)
        elif topic == "sports":
            return TweetGenerator.generate_sports_tweets(count=100000, from_date=from_date, end_date=end_date)
        elif topic == "cinema":
            return TweetGenerator.generate_cinema_tweets(count=100000, from_date=from_date, end_date=end_date)
        else:
            return TweetGenerator.generate_travel_tweets(count=100000, from_date=from_date, end_date=end_date)


class InstagramFetcher:
    def __init__(self):
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.account_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
        self.base_url = "https://graph.facebook.com/v18.0"

    def fetch_top_media(self, hashtag="travel"):
        """
        Fetches top media for a hashtag to find related locations.
        Requires Instagram Graph API setup.
        """
        if not self.access_token or not self.account_id:
            print("Instagram credentials missing. Returning mock data.")
            return self._get_mock_data()

        try:
            # 1. Get Hashtag ID
            search_url = f"{self.base_url}/ig_hashtag_search"
            params = {
                "user_id": self.account_id,
                "q": hashtag,
                "access_token": self.access_token
            }
            response = requests.get(search_url, params=params)
            data = response.json()
            
            if 'data' not in data or not data['data']:
                return []
            
            hashtag_id = data['data'][0]['id']

            # 2. Get Top Media for Hashtag
            media_url = f"{self.base_url}/{hashtag_id}/top_media"
            media_params = {
                "user_id": self.account_id,
                "fields": "caption,children,media_type,media_url,permalink",
                "access_token": self.access_token
            }
            media_response = requests.get(media_url, params=media_params)
            media_data = media_response.json()

            locations = []
            if 'data' in media_data:
                for post in media_data['data']:
                    if 'caption' in post:
                        locations.append(post['caption'][:50] + "...") 
            return locations

        except Exception as e:
            print(f"Error fetching Instagram data: {e}")
            return []

    def _get_mock_data(self):
        return ["Sunset in Oia", "Hiking in Patagonia", "Beach day in Maldives", "City lights of Tokyo"]


class NewsFetcher:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_travel_news(self):
        if not self.api_key:
            print("News API key missing. Returning mock data.")
            return self._get_mock_data()

        try:
            params = {
                "q": "travel OR tourism OR vacation",
                "sortBy": "popularity",
                "language": "en",
                "apiKey": self.api_key,
                "from": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            }
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            headlines = []
            if 'articles' in data:
                for article in data['articles']:
                    headlines.append(article['title'])
            return headlines
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def _get_mock_data(self):
        return [
            "Top 10 destinations to visit this summer",
            "Why Lisbon is the new digital nomad capital",
            "Hidden gems in Southeast Asia",
            "Travel restrictions update for Europe"
        ]
