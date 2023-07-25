import pytest
from app import create_app
from models.models import TestDB, db
from models.cards import Card


@pytest.fixture(scope='session')
def app():
    # Setup
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        db.create_all()

    yield app

    # Teardown
    with app.app_context():
        # Clear all records from TestDB
        db.session.query(TestDB).delete()
        db.session.commit()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope='session')
def generic_card(app):
    with app.app_context():
        # Setup
        new_card = Card(
            card_name='Testing Cards',
            card_description='Lorem Ipsum...')

        db.session.add(new_card)
        db.session.commit()

        yield new_card
        # Teardown
        db.session.delete(new_card)
        db.session.commit()
