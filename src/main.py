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
import twitter
from tweed import Tweed

def __main__():
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/conf')
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    log = logging.getLogger("Main")
    config = ConfigParser.SafeConfigParser()
    try:
        config.read('../conf/config.cfg')
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
    while True:
        tweed.close_friend_gap()

        #see if anyone has sent any new feeds
        last_dm_qry = db_session.query(Feed.twitter_dm_id).order_by(Feed.created_at_in_seconds)

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
                entries = feedmonitor.find_new_entries(i)
            except feedmonitor.NotValidFeed as e:
                log.error(e)
                #if we can't use this feed, delete it
                db_session.delete(i)

            if entries == None:
                continue;

            for e in entries:
                log.debug("date for feed %s: %s", e.title, e.updated_parsed)
                log.debug("last update for feed: %s", time.gmtime(i.processed_date))

            db_session.begin()
            i.processed_date = datetime.now()
            try:
                tweed.notify_followers(i.twitter_user_id, entries, i.feed_title)
            except Exception as e:
                log.error(e)
                db_session.rollback()
            db_session.commit()

            del entries


        
        time.sleep(20)



if __name__ == '__main__':
    __main__()
