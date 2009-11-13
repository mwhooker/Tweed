import sys
import os
import time
import logging
from supay import Daemon
from tweed import Tweed
from feed import Feed
import feedmonitor
from databasehandle import Session
from datetime import datetime

def run():
    initial_program_setup()
    daemon = Daemon(name='tweed')
    daemon.start()
    do_tweed_loop()

def stop():
    daemon.stop()


def do_tweed_loop():
    db_session = Session()
    tweed = Tweed()
    log = logging.getLogger("Main")
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


def initial_program_setup():
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/conf')

def program_cleanup():
    return


def reload_program_config():
    return


if __name__ == '__main__':
    initial_program_setup()
    do_tweed_loop()
