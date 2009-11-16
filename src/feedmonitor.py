import feedparser
import logging
import datetime, time

class NotValidFeed(Exception):
    pass

class NoEntries(Exception):
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
        self.last_modified_date = self.findLastModifiedDate(feed)


    def getEntries(self,since):
        if self.updated == False:
            return None
    
        feed = cache.get(self.url)
        
        if len(feed.entries) < 1:
            raise NoEntries

        e = feed.entries

        new_entries = [i for i in e if since < 
                self.last_modified_date]

        logging.info("found %d new posts to process", len(new_entries))

        return new_entries

    def findLastModifiedDate(self, feedObj):
        if feedObj.has_key('updated_parsed'):
            return feedObj.updated_parsed

        if len(feedObj.entries) < 1:
            raise NoEntries

        feedObj.entries.sort(
                key=lambda x: x['updated_parsed'], 
                reverse=True
                )

        last_entry = feedObj.entries[0]
        if last_entry.has_key('updated_parsed'):
            return last_entry.updated_parsed
        if last_entry.has_key('published_parsed'):
            return last_entry.published_parsed

        raise NotValidFeed

            

class FeedCache(object):
    
    def __init__(self, fp):
        self.cache = {}
        self.feedparser = fp

    def valid(self,url):
        if url in self.cache:
            feed = self.feedparser.parse(url, 
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

    def remove(self, url):
        del self.cache[url]


cache = FeedCache(feedparser)
