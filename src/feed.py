from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.databases import sqlite
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import datetime

Base = declarative_base()
class Feed(Base):
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True)
    twitter_user_id = Column(Integer)
    url = Column(String)
    twitter_dm_id = Column(Integer)
    created_at_in_seconds = Column(Integer)
    processed_date = Column(sqlite.SLDateTime)

    def __init__(self, twitter_dm_id, twitter_id, created_at_in_seconds, url):
        self.created_at_in_seconds = created_at_in_seconds
        self.twitter_dm_id = twitter_dm_id
        self.twitter_user_id = twitter_id
        self.url = url
        self.processed_date = datetime.datetime.now() - datetime.timedelta(days=1)
        #self.date_received = 

    def __repr__(self):
        return "<Feed('%s','%s')>" % (self.twitter_id, self.url)
    
