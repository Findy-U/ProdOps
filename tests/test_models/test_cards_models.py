from models.cards import CardAssignees, CardLabels, CardMovements
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


def test_add_labels(generic_card):
    label = CardLabels(
        label_name='First Issue',
        card_id=generic_card.card_id
    )

    db.session.add(label)
    db.session.commit()

    assert label.card_id == generic_card.card_id
    assert generic_card.card_labels[0].assignee_id == label.assignee_id


def test_add_movements(generic_card):
    pass
