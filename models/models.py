from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

db = SQLAlchemy()

Base = declarative_base()


class Alldata(Base):
    __tablename__ = 'alldata'

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    project_card_id = db.Column(db.Text)
    status = db.Column(db.Text)
    assignee = db.Column(db.Text)
