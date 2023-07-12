from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Alldata(db.Model):
    """ There's only one attribute in this class using nullable as true.
        It's good to notice that in DB all attributes are nullable except
        by record_key, that is the primary key. """

    __tablename__ = 'alldata'

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    project_card_id = db.Column(db.Text)
    status = db.Column(db.Text)
    assignee = db.Column(db.Text)
