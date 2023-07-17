from payload_example.full_payload_example import full_payload
from payload_example.issue_opened import issue_opened
from webhook.process_hook import process_webhook
from webhook.parse_issue import parse_issue

from models.models import db, TestDB


def test_send_payload_to_webhook(client) -> None:
    """ Sends the ping payload from GitHub
        that leads to an expected error. """

    response = client.post('/payload', json=full_payload)
    assert response.status_code == 400


def test_issue_opened_and_updated(client) -> None:
    new_issue = {
        "action": "opened",
        "issue": {
            "project_card_id": "1012020302023",
            "assignee": 'Demian143',
            "assignee_login": 'Demian143',
            "created_at": "2023-07-14T02:18:42Z",
            "closed_at": None
        }
    }

    response = client.post('/payload', json=new_issue)
    assert response.status_code == 201

    # Update issue
    new_issue['issue']['closed_at'] = '2023-07-17T00:33:45Z'
    response = client.post('/payload', json=new_issue)
    assert response.status_code == 204


def test_issue_opened(app) -> None:
    # Get project card id to query in db
    issue_parsed = parse_issue(issue_opened.get('issue'))

    with app.app_context():
        assert process_webhook(issue_opened) == ('resource created', 201)

        check_record_exists = db.session.query(TestDB).filter_by(
            project_card_id=issue_parsed.get('project_card_id')).first()

        assert check_record_exists.project_card_id == issue_parsed.get(
            'project_card_id')
