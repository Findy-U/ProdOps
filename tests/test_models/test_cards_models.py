from models.cards import CardAssignees
from models.models import db


def test_create_generic_card(generic_card):
    assert type(generic_card.card_id) is int


def test_add_assignee_to_card(generic_card):
    assignee = CardAssignees(
        assignee_name='Demian143',
        card_id=generic_card.card_id
    )

    db.session.add(assignee)
    db.session.commit()

    assert assignee.card_id == generic_card.card_id
    assert generic_card.card_assignees[0].assignee_id == assignee.assignee_id

    # Teardown
    db.session.delete(assignee)
    db.session.commit()
