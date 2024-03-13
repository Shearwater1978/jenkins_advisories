import unittest

from unittest.mock import patch, MagicMock
from rss_feed_reader import get_news_feed_status, get_latest_feed


class TestGetNewsFeedStatus(unittest.TestCase):
    @patch(rss_feed_reader.get_news_feed_status, 'get_news_feed_status')
    def test_rss_feed_reader(self, get_news_feed_status):
        get_news_feed_status.return_value = False
        result = get_latest_feed(1)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
