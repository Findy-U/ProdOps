from .models import db


class Cards(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Possible length of a card title
    card_name = db.Column(db.String(500), nullable=False)
    card_description = db.Column(db.Text, nullable=True)
    # Relationships
    card_movements = db.relationship(
        'CardMovements', backref='cards', lazy=True)
    card_assignees = db.relationship(
        'CardAssignees', backref='cards', lazy=True)
    card_labels = db.relationship(
        'CardLabels', backref='cards', lazy=True)


class CardMovements(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    origin_column = db.Column(db.String(200), nullable=False)
    destination_column = db.Column(db.String(200), nullable=False)
    movement_date_time = db.Column(db.DateTime, nullable=False)
    # Foreign Key
    card_id = db.Column(db.Integer, db.ForeignKey(
        'cards.card_id'), nullable=False)


class CardAssignees(db.Model):
    assignee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assignee_name = db.Column(db.String(200), nullable=False)
    assignee_date_time = db.Column(db.DateTime)
    # Foreign Key
    card_id = db.Column(db.Integer, db.ForeignKey(
        'cards.card_id'), nullable=False)


class CardLabels(db.Model):
    label_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label_name = db.Column(db.String(200), nullable=False)
    label_date_time = db.Column(db.DateTime, nullable=False)
    # Foreign Key
    card_id = db.Column(db.Integer, db.ForeignKey(
        'cards.card_id'), nullable=False)
