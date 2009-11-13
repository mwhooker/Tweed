from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from feed import Feed


engine = create_engine('sqlite:///', echo=True)
Session = sessionmaker(bind=engine, autocommit=True, autoflush=True)
Feed.metadata.create_all(engine)
