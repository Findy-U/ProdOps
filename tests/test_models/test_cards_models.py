from models.cards import Cards
from models.models import db


def test_create_new_card(app):
    with app.app_context():
        new_card = Cards(
            card_name='Testing Cards',
            card_description='Lorem Ipsum...')

        db.session.add(new_card)
        db.session.commit()

        assert type(new_card.card_id) is int

        # Delete Test Record
        db.session.delete(new_card)
        db.session.commit()


"""
def test_add_assignee_to_card():
    return
"""
