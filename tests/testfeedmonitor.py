import unittest, os
from mock import Mock, patch
import feedmonitor
import time


class TestFeedCache(unittest.TestCase):
    url = 'http://example.net'
    
    def setUp(self):
        self.mockfeed = Mock()
        self.mockfeed.modified = 'xxx'
        self.mockfeed.etag = 'yyy'


    def testValidity200(self):
        self.mockfeed.status=200
        with patch('feedmonitor.feedparser.parse') as MockParse:
            MockParse.return_value = self.mockfeed
            feedmonitor.cache.set(self.url, self.mockfeed)
            self.assertFalse(feedmonitor.cache.valid(self.url))

    def testValidity304(self):
        self.mockfeed.status=304
        with patch('feedmonitor.feedparser.parse') as MockParse:
            MockParse.return_value = self.mockfeed
            feedmonitor.cache.set(self.url, self.mockfeed)
            self.assert_(feedmonitor.cache.valid(self.url))

    def testCaching(self):
        '''make sure feedparser is taken from cache the second time'''
        with patch('feedmonitor.feedparser.parse') as MockParse:
            self.mockfeed.feed.title = 'title'
            self.mockfeed.status = 304
            MockParse.return_value = self.mockfeed

            lhs = feedmonitor.FeedMonitor(self.url)
            self.assertEqual(MockParse.call_args, ((self.url,), {}))
            rhs = feedmonitor.FeedMonitor(self.url)
            self.assertEqual(MockParse.call_args, ((self.url,), {'etag': 'yyy', 'modified': 'xxx'}))




class TestFeedMonitor(unittest.TestCase):
    fixture_path = os.path.dirname(os.path.abspath(__file__)) + '/fixtures'

    def testGetEntries(self):
        feed = feedmonitor.FeedMonitor(self.fixture_path + '/3item.xml') 
        since = time.strptime("01 Aug 2006", "%d %b %Y")
        self.assertEquals(len(feed.getEntries(since)), 2)
