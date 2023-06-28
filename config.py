from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import dotenv
import os

# This line is being loaded at the start of the app.py, no need for duplicates
dotenv.load_dotenv('.env')

ssl_args = {
    'ssl': {
        'ca': os.getenv('SSL_PATH')
    }
}

DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

engine = create_engine(DATABASE_URI, connect_args=ssl_args)
session = sessionmaker(bind=engine)
