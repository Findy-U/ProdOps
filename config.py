from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

ssl_args = {
    'ssl': {
        'ca': os.environ['SSL_PATH']
    }
}

DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

engine = create_engine(DATABASE_URI, connect_args=ssl_args)
session = sessionmaker(bind=engine)
