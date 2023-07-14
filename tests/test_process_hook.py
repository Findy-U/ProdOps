from payload_example.full_payload_example import full_payload
from payload_example.issue_opened import issue_opened
from webhook.process_hook import process_webhook
from webhook.parse_issue import parse_issue

from models.models import db, TestDB


def test_send_payload_to_webhook(client) -> None:
    response = client.post('/payload', json=full_payload)
    assert response.status_code == 200


def test_issue_opened(app) -> None:
    # Get project card id to query in db
    issue_parsed = parse_issue(issue_opened.get('issue'))

    with app.app_context():
        assert process_webhook(issue_opened, test=True) is None

        check_record_exists = db.session.query(TestDB).filter_by(
            project_card_id=issue_parsed.get('project_card_id')).first()

        assert check_record_exists.project_card_id == issue_parsed.get(
            'project_card_id')
