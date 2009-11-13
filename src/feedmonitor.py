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
    #not comparing correctly
#    new_entries = [i for i in e if 
 #       feedObj.processed_date < datetime.datetime.fromtimestamp(time.mktime(i.updated_parsed))]
    new_entries = [i for i in e if 
        time.gmtime(feedObj.processed_date) < i.updated_parsed]

    logging.info("found %d new feeds to process", len(new_entries))


    return new_entries
