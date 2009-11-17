from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *
from sqlalchemy import Table, Column

import datetime
import time

Base = declarative_base()
class Feed(Base):
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True)
    twitter_user_id = Column(Integer)
    url = Column(String)
    twitter_dm_id = Column(Integer)
    created_at_in_seconds = Column(Integer)
    processed_date = Column(PickleType)

    def __init__(self, twitter_dm_id, twitter_id, created_at_in_seconds, url):
        self.created_at_in_seconds = created_at_in_seconds
        self.twitter_dm_id = twitter_dm_id
        self.twitter_user_id = twitter_id
        self.url = url
        self.processed_date = time.gmtime()
        #self.date_received = 

    def __repr__(self):
        return "<Feed('%s','%s')>" % (self.twitter_id, self.url)
    
