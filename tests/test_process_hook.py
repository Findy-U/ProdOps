from payload_example.full_payload_example import full_payload
from payload_example.issue_opened import issue_opened
from payload_example.issue_closed import issue_closed
from payload_example.issue_reopened import issue_reopened
from webhook.parse_issue import parse_issue

from models.models import db, TestDB


def test_send_payload_to_webhook(client) -> None:
    """ Sends the ping payload from GitHub
        that leads to an expected error. """

    response = client.post('/payload', json=full_payload)
    assert response.status_code == 400


def test_issue_opened(client, app) -> None:
    response = client.post('/payload', json=issue_opened)
    assert response.status_code == 201


def test_issue_closed(client) -> None:
    # Open issue
    client.post('/payload', json=issue_opened)
    # Close issue
    response = client.post('/payload', json=issue_closed)
    assert response.status_code == 204


def test_issue_reopened(client) -> None:
    # Open issue
    client.post('/payload', json=issue_opened)
    # Close issue
    client.post('/payload', json=issue_closed)
    # Reopen Issue
    response = client.post('/payload', json=issue_reopened)
    assert response.status_code == 204


def test_verify_if_data_persisted(client, app) -> None:
    client.post('/payload', json=issue_opened)

    with app.app_context():
        # Get project card id to query in db
        issue_parsed = parse_issue(issue_opened.get('issue'))
        # Verify if data persisted
        check_record_exists = db.session.query(TestDB).filter_by(
            project_card_id=issue_parsed.get('project_card_id')).first()

        assert check_record_exists.project_card_id == issue_parsed.get(
            'project_card_id')
