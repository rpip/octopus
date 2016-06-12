import os
from datetime import datetime

from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

CLOUDSQL_PROJECT = os.getenv('OCTOPUS_PROJECT')
CLOUDSQL_INSTANCE = os.getenv('OCTOPUS_SQLINSTANCE')
DB_NAME = os.getenv('OCTOPUS_DBNAME')

Base = declarative_base()


def db_url():
    if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
        return 'mysql+mysqldb://root@/%s?unix_socket=/cloudsql/%s:%s'.format(
            DB_NAME, CLOUDSQL_PROJECT, CLOUDSQL_INSTANCE)
    else:
        return 'mysql+mysqldb://root:@localhost/octopus'.format(DB_NAME)


class WordCount(Base):

    __tablename__ = 'wordcount'

    uuid = Column(String(255), primary_key=True)
    word = Column(String(255), nullable=False)
    count = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, word, count):
        # TODO: hash uuid and encrypt/decrypt word
        self.uuid = word
        self.word = word
        self.count = count


def init_db():
    "Initializes the database and creates the tables"
    engine = create_engine(db_url())
    Base.metadata.create_all(bind=engine)
    return scoped_session(sessionmaker(bind=engine))
