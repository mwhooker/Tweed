from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
class Feed(Base):
    __tablename__ = 'feeds'

    feed_id = Column(Integer, primary_key=True)
    twitter_user_id = Column(Integer)
    url = Column(String)
    twitter_dm_id = Column(Integer)

    def __init__(self, twitter_id, url):
        self.twitter_id = twitter_id
        self.url = url
        #self.date_received = 

    def __repr__(self):
        return "<Feed('%s','%s')>" % (self.twitter_id, self.url)
    
