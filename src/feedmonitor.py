import feedparser
import logging
import datetime, time

class NotValidFeed(Exception):
    pass

class FeedMonitor(object):

    updated = False
    new_entries = None

    def __init__(self, url):
        self.url = url 
        if cache.valid(url):
            return

        self.updated = True

        feed = feedparser.parse(url)
        cache.set(url, feed)

        self.title = feed.feed.title
        self.last_modified_date = feed.feed.updated_parsed


    def getEntries(self,since):
        if self.updated == False:
            return None
    
        feed = cache.get(self.url)
        e = feed.entries

        new_entries = [i for i in e if time.gmtime(since) < self.last_modified_date]
        logging.info("found %d new posts to process", len(new_entries))

        return new_entries

class FeedCache(object):
    
    def __init__(self):
        self.cache = {}

    def valid(self,url):
        if url in self.cache:
            feed = feedparser.parse(url, 
                    modified=self.cache[url].modified, 
                    etag=self.cache[url].etag
                    )
            if feed.status == 304:
                return True

        return False 


    def set(self,url, feedObj):
        self.cache[url] = feedObj

    def get(self,url):
        return self.cache[url]


cache = FeedCache()
