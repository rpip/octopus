import os
from datetime import datetime
import hashlib

from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

CLOUDSQL_PROJECT = 'octopus-1340'
CLOUDSQL_INSTANCE = 'octopus'
DB_NAME = 'octopus'

PK_KEY_SALT = os.getenv('OCTOPUS_SALT', '123456')

Base = declarative_base()


def db_url():
    if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
        return 'mysql+mysqldb://root@/%s?unix_socket=/cloudsql/%s:%s'.format(
            DB_NAME, CLOUDSQL_PROJECT, CLOUDSQL_INSTANCE)
    else:
        return 'mysql+mysqldb://root:@localhost/octopus'.format(DB_NAME)


def generate_uuid(word):
    """Generates a unique ID as primary key from the given word"""
    m = hashlib.sha1()
    m.update(PK_KEY_SALT)
    m.update(word)
    return m.hexdigest()


class WordCount(Base):

    __tablename__ = 'wordcount'

    uuid = Column(String(255), primary_key=True)
    word = Column(String(255), nullable=False)
    count = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, word, count, uuid):
        # TODO: hash uuid and encrypt/decrypt word
        self.uuid = uuid or generate_uuid(word)
        self.word = word
        self.count = count


def init_db():
    "Initializes the database and creates the tables"
    engine = create_engine(db_url())
    Base.metadata.create_all(bind=engine)
    return scoped_session(sessionmaker(bind=engine,
                          autocommit=False,
                          autoflush=True))
