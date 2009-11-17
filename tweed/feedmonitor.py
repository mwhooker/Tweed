import feedparser
import logging
import datetime, time

class NotValidFeed(Exception): pass
class NoEntries(Exception): pass

class FeedMonitor(object):
    '''perform date-range queries on RSS/ATOM feeds'''


    updated = False
    new_entries = None

    def __init__(self, uri):
        self.uri = uri 
        if cache.valid(uri):
            return

        self.updated = True

        feed = feedparser.parse(uri)
        cache.set(uri, feed)

        self.title = feed.feed.title
        self.last_modified_date = self.findLastModifiedDate(feed)


    def getEntries(self,since):
        if self.updated == False:
            return None

        if type(since) != time.struct_time:
            raise TypeError
    
        feed = cache.get(self.uri)
        
        if len(feed.entries) < 1:
            raise NoEntries

        e = feed.entries

        new_entries = [i for i in e if since < 
                i.updated_parsed]

        logging.info("found %d new posts to process", len(new_entries))

        return new_entries

    def findLastModifiedDate(self, feedObj):
        if feedObj.has_key('updated'):
            return feedObj.updated

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
    '''cache feedparse object, respecting remote servers' 
    etag/last-modified headers'''
    
    def __init__(self):
        self.cache = {}

    def valid(self,uri):
        '''is the feedparser handle still valid, or has the resource
        been modified?'''

        if uri in self.cache:
            if self.cache[uri].has_key('modified'):
                mod = self.cache[uri].modified
            else:
                mod = None
            
            if self.cache[uri].has_key('etag'):
                etag = self.cache[uri].etag
            else:
                etag = None

            feed = feedparser.parse(uri, modified=mod, etag=etag)

            if feed.status == 304:
                return True

        return False 


    def set(self,uri, feedObj):
        self.cache[uri] = feedObj

    def get(self,uri):
        return self.cache[uri]

    def remove(self, uri):
        del self.cache[uri]



cache = FeedCache()
