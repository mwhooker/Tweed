from sqlite3 import dbapi2 as sqlite
import sys
import os
import time
import logging
from supay import Daemon
from tweed import Tweed
from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from feed import Feed

class DatabaseHandle:

    def __init__(self):
        engine = create_engine('sqlite:///file.db', module=sqlite, echo=True)
        Feed.metadata.create_all(engine)
        self.session = create_session(bind=engine, autocommit=True)
        self.log = logging.getLogger('db')

    def last_processed_feed(self):
        qry = self.session.query(Feed.twitter_dm_id).order_by(Feed.created_at_in_seconds)
        if qry.count() > 0:
            last_id = qry.first()
            self.log.info('last processed id was: %d', last_id.twitter_dm_id)
            return last_id


    def process_feeds(self, feeds):
        self.log.info('processing %d feeds into db', len(feeds)) 
        print feeds
        self.session.add_all(feeds)
        print self.last_processed_feed()



def run():
    initial_program_setup()
    daemon = Daemon(name='tweed')
    daemon.start()
    do_tweed_loop()

def stop():
    daemon.stop()


def do_tweed_loop():
    db = DatabaseHandle()
    tweed = Tweed()
    while True:
        tweed.close_friend_gap()
        last_dm = db.last_processed_feed()
        print "last dm is %s" % last_dm
        feeds = tweed.get_feed_requests(last_dm)
        db.process_feeds(feeds)

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
