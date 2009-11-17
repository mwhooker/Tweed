import sys
import os
import time
import logging
import tweed
import ConfigParser
from feed import Feed
import feedmonitor
from databasehandle import Session
from datetime import datetime
from bitly import Bitly
import twitter, simplejson
from tweed import Tweed

#incase twitter goes does. as suggested here:
#http://code.google.com/p/python-twitter/issues/detail?id=92
import socket
socket.setdefaulttimeout(60)


CONFIG_PATH = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))) + '/conf'

def __main__():
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger("Main")
    config = ConfigParser.SafeConfigParser()
    try:
        config.read(CONFIG_PATH + '/config.cfg')
    except config.ParsingError as e:
        logging.error("uh oh parsing error: %s", e)

    twitterApi = twitter.Api(
            username=config.get('Twitter User', 'screen_name'), 
            password=config.get('Twitter User', 'password')
            )
    bitly = Bitly(
            config.get('bitly', 'login'),
            config.get('bitly', 'apiKey')
            )
    tweed = Tweed(twitterApi, bitly)

    db_session = Session()

    Continue = True
    while Continue:

        tweed.close_friend_gap()
        try:
            log.debug("API calls left: %d", 
                tweed.twitter.RateLimitStatus()['remaining_hits'])
        except Exception as e:
            log.error(e)

        #see if anyone has sent any new feeds
        last_dm_qry = db_session.query(Feed.twitter_dm_id).order_by(
                Feed.twitter_dm_id.desc())

        if last_dm_qry.count():
            last_dm = last_dm_qry.first().twitter_dm_id 
            log.info('last processed id was: %d', last_dm)
        else:
            last_dm = None

        new_feeds = tweed.get_feed_requests(last_dm)

        if new_feeds:
            db_session.add_all(new_feeds)
            log.info('processing %d feeds into db', len(new_feeds)) 


        #process new feed entries
        current_feeds = db_session.query(Feed).all()
        for i in current_feeds:
            try:
                feed = feedmonitor.FeedMonitor(i.url)
#                entries = feedmonitor.find_new_entries(i)
            except feedmonitor.NotValidFeed as e:
                log.error(e)
                #if we can't use this feed, delete it
                db_session.delete(i)
                continue
            except Exception as e:
                log.error(e)
                continue

            if feed.updated == False:
                continue;

            entries = feed.getEntries(i.processed_date)

            log.info("%s updated with %d new entries", 
                    feed.title, len(entries))

            db_session.begin()
            i.processed_date = feed.last_modified_date
            try:
                tweed.notify_followers(
                        i.twitter_user_id, entries, feed.title)
            except Exception as e:
                log.error(e)
                db_session.rollback()
            db_session.commit()

            del entries

        time.sleep(120)



#patch twitter API with rape_limit_status method
def rate_limit_status(self):
    url = 'http://twitter.com/account/rate_limit_status.json'
    json = self._FetchUrl(url)
    data = simplejson.loads(json)
    self._CheckForTwitterError(data)
    return data

twitter.Api.RateLimitStatus = rate_limit_status

if __name__ == '__main__':
    __main__()
