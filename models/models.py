from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Card(db.Model):
    """ There's only one attribute in this class using nullable as true.
        It's good to notice that in DB all attributes are nullable except
        by record_key, that is the primary key. """

    __tablename__ = 'card'

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    closed_at = db.Column(db.DateTime, nullable=True)
    project_card_id = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)  # Open, Closed or Reopened
    assignee = db.Column(db.Text, nullable=True)
    # New colums
    repository = db.Column(db.Text, nullable=False)


class TestDB(db.Model):
    __test__ = False
    __tablename__ = 'test_db'

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    closed_at = db.Column(db.DateTime, nullable=True)
    project_card_id = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)  # Open, Closed or Reopened
    assignee = db.Column(db.Text, nullable=True)
    # New colums
    repository = db.Column(db.Text, nullable=False)
