import unittest
from mock import Mock
from feedmonitor import *


class TestFeedCache(unittest.TestCase):
    mockfeed = Mock()
    url = 'http://example.net'
    
    def setUp(self):
        self.mockfeed.modified = 'xxx'
        self.mockfeed.etag = 'yyy'


    def testValidity200(self):
        mockfeedparser = Mock()
        mockfeedparser.parser.status.return_value = 200
        cache200 = FeedCache(mockfeedparser)
        cache200.set(self.url, self.mockfeed)

        self.assertFalse(cache200.valid(self.url))

    def testValidity304(self):
        mockfeedparser = Mock()
        mockfeedparser.parser.status.return_value = 304
        cache304 = FeedCache(mockfeedparser)
        cache304.set(self.url, self.mockfeed)

        self.assertFalse(cache304.valid(self.url))


class TestFeedMonitor(unittest.TestCase):
    pass
