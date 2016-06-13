import os
import hashlib
from base64 import b64encode
from datetime import datetime

from sqlalchemy import (
    create_engine, Column, String, Integer,
    DateTime, LargeBinary
)
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from Crypto.PublicKey import RSA

PK_KEY_SALT = os.getenv('OCTOPUS_SALT',
                        b64encode(os.urandom(64)).decode('utf-8'))

# asymmetric encrytion
RSA_KEYFILE = os.path.join(os.path.dirname(__file__), 'rsakeyfile')
RSA_KEY = RSA.importKey(open(RSA_KEYFILE, 'r').read())
RSA_PUBLIC_KEY = RSA_KEY.publickey()


# GAE CloudSQL
CLOUDSQL_PROJECT = 'octopus-1340'
CLOUDSQL_INSTANCE = 'octopus'
DB_NAME = 'octopus'
DB_USER = os.getenv('MYSQL_USER')
DB_HOST = os.getenv('MYSQL_HOST')

Base = declarative_base()


def db_url():
    if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
        _url = 'mysql+mysqldb://{0}@/{1}?unix_socket=/cloudsql/{2}:{3}'
        return _url.format(DB_USER, DB_NAME, CLOUDSQL_PROJECT,
                           CLOUDSQL_INSTANCE)
    else:
        return 'mysql+mysqldb://{0}:@{1}/{2}'.format(DB_USER, DB_HOST, DB_NAME)


def generate_uuid(word):
    """Generates a unique ID as primary key from the given word"""
    m = hashlib.sha1()
    m.update(PK_KEY_SALT)
    m.update(word)
    return m.hexdigest()


class WordCount(Base):

    __tablename__ = 'wordcount'

    uuid = Column(String(255), primary_key=True)
    word = Column(LargeBinary(), nullable=False)
    count = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, word, count, uuid):
        # TODO: hash uuid and encrypt/decrypt word
        self.uuid = uuid or generate_uuid(word)
        self.word = self._encrypt(word)
        self.count = count

    def _encrypt(self, word):
        return RSA_PUBLIC_KEY.encrypt(str(word), 32)[0]

    def _decrypt(self):
        return RSA_KEY.decrypt(self.word)

    @property
    def as_raw(self):
        return self._decrypt()


def init_db():
    "Initializes the database and creates the tables"
    engine = create_engine(db_url())
    Base.metadata.create_all(bind=engine)
    return scoped_session(sessionmaker(bind=engine,
                          autocommit=False,
                          autoflush=True))
