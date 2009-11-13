import feedparser
import logging
import datetime, time

class NotValidFeed(Exception):
    pass

def find_new_entries(feedObj):
    d = feedparser.parse(feedObj.url)

    if feedObj.feed_title != d.feed.title:
        feedObj.feed_title = d.feed.title

    e = d.entries
    new_entries = [i for i in e if 
        feedObj.processed_date < datetime.datetime.fromtimestamp(time.mktime(i.updated_parsed))]

    logging.info("found %d new feeds to process", len(new_entries))

    return new_entries
