from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from feed import Feed


#add to physical file when done
engine = create_engine('sqlite:///tweed.db', echo=False)
Session = sessionmaker(bind=engine, autocommit=True, autoflush=True)
Feed.metadata.create_all(engine)

