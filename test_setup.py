import unittest
from fetchers import TwitterFetcher, InstagramFetcher, NewsFetcher

class TestSocialMediaAnalyser(unittest.TestCase):
    def setUp(self):
        print("\nSetting up test...")

    def test_twitter_fetcher(self):
        print("Testing TwitterFetcher...")
        fetcher = TwitterFetcher()
        trends = fetcher.fetch_trends()
        self.assertIsInstance(trends, list)
        print(f"Twitter returned {len(trends)} items.")

    def test_instagram_fetcher(self):
        print("Testing InstagramFetcher...")
        fetcher = InstagramFetcher()
        media = fetcher.fetch_top_media()
        self.assertIsInstance(media, list)
        print(f"Instagram returned {len(media)} items.")

    def test_news_fetcher(self):
        print("Testing NewsFetcher...")
        fetcher = NewsFetcher()
        news = fetcher.fetch_travel_news()
        self.assertIsInstance(news, list)
        print(f"News returned {len(news)} items.")

if __name__ == '__main__':
    unittest.main()
