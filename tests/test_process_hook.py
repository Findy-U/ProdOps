from payload_example.full_payload_example import full_payload
from payload_example.issue_opened import issue_opened
from payload_example.issue_closed import issue_closed
from payload_example.issue_reopened import issue_reopened
from webhook.parse_issue import parse_issue

from models.models import db, TestDB

""" Fixture scoped as 'session'. Every test assumes the
    action the last test took persisted.
    Can be resumed:
        - Send ping payload.
        - Open issue.
        - Close issue.
        - Reopen issue.
        - Verify if data really persisted. """


def test_send_payload_to_webhook(client) -> None:
    """ Sends the ping payload from GitHub
        that leads to an expected error. """

    response = client.post('/payload', json=full_payload)
    assert response.status_code == 400


def test_issue_opened(client, app) -> None:
    response = client.post('/payload', json=issue_opened)
    assert response.status_code == 201


def test_issue_closed(client) -> None:
    response = client.post('/payload', json=issue_closed)
    assert response.status_code == 204


def test_issue_reopened(client) -> None:
    response = client.post('/payload', json=issue_reopened)
    assert response.status_code == 204


def test_verify_if_data_persisted(client, app) -> None:
    # Get project card id to query in db
    issue_parsed = parse_issue(issue_opened.get('issue'))

    with app.app_context():
        # Verify if data persisted
        check_record_exists = db.session.query(TestDB).filter_by(
            project_card_id=issue_parsed.get('project_card_id')).first()

        assert check_record_exists.project_card_id == issue_parsed.get(
            'project_card_id')
