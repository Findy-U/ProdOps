from .models import db

card_labels = db.Table('card_labels',
                       db.Column('card_id', db.Integer, db.ForeignKey(
                           'card.card_id'), primary_key=True),
                       db.Column('label_id', db.Integer, db.ForeignKey(
                           'label.label_id'), primary_key=True)
                       )


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Possible length of a card title
    card_name = db.Column(db.String(500), nullable=False)
    card_description = db.Column(db.Text)
    # Relationships
    card_movements = db.relationship(
        'CardMovements', backref='cards', lazy=True)
    card_assignees = db.relationship(
        'CardAssignees', backref='cards', lazy=True)
    # Many-to-Many
    card_label = db.relationship(
        'Label',
        secondary=card_labels,
        lazy='subquery',
        backref=db.backref('cards', lazy=True))


class Label(db.Model):
    label_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label_name = db.Column(db.String(200), nullable=False)
    label_date_time = db.Column(db.DateTime)


class CardMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    origin_column = db.Column(db.String(200))
    destination_column = db.Column(db.String(200))
    movement_date_time = db.Column(db.DateTime)
    # Foreign Key
    card_id = db.Column(db.Integer, db.ForeignKey(
        'cards.card_id'))


class CardAssignee(db.Model):
    assignee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assignee_name = db.Column(db.String(200), nullable=False)
    assignee_date_time = db.Column(db.DateTime)
    # Foreign Key
    card_id = db.Column(db.Integer, db.ForeignKey(
        'cards.card_id'))
