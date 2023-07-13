from models.models import Alldata, TestDB
from logger.logger import logger
from .parse_issue import parse_issue
from models.models import db

# Logger
logger = logger()


def process_webhook(data: dict, test=False) -> None:
    # logger.info('Type and value of data: %s, %s', type(data), data)
    db_instance = Alldata

    if test:
        db_instance = TestDB

    action = data.get('action')
    issue = data.get('issue')

    if not issue:
        logger.error(
            "Invalid payload structure. Skipping webhook processing.")
        db.session.close()
        return

    parsed_issue = parse_issue(issue)

    if action == 'reopened':
        issue_reopened(parsed_issue, db_instance)
        return

    if action in ['opened', 'assigned', 'closed', 'reordered', 'edited']:
        issue_create_or_edit(parsed_issue, db_instance)
        return

    else:
        logger.error(
            "Unsupported action: %s. Skipping webhook processing.", action)
        return


def issue_reopened(parsed_issue: dict, db_instance) -> None:
    project_card_id = parsed_issue['project_card_id']

    existing_data = db.session.query(db_instance).filter_by(
        project_card_id=project_card_id).first()

    existing_data.closed_at = None
    existing_data.status = 'Maintenance'

    db.session.add(existing_data)
    db.session.commit()
    logger.info(
        'Issue reopened successfully for record_id: %s',
        existing_data.record_id)

    return


def issue_create_or_edit(parsed_issue: dict, db_instance) -> None:
    closed_at = parsed_issue["closed_at"]
    project_card_id = parsed_issue["project_card_id"]
    assignee_login = parsed_issue["assignee_login"]
    created_at = parsed_issue["created_at"]

    status = 'open' if closed_at is None else 'closed'

    existing_data = db.session.query(db_instance).filter_by(
        project_card_id=project_card_id).first()

    if existing_data:
        if assignee_login:
            existing_data.assignee = assignee_login
        if closed_at:
            existing_data.closed_at = closed_at
        if created_at:
            existing_data.created_at = created_at
        if status:
            existing_data.status = status

        db.session.commit()
        logger.info(
            'Data updated successfully for record_id: %s',
            existing_data.record_id)

        return

    else:
        logger.info(
            'No existing data found for project_card_id: %s',
            project_card_id)

        all_data = db_instance(
            project_card_id=project_card_id,
            created_at=created_at,
            closed_at=closed_at,
            status=status,
            assignee=assignee_login
        )
        db.session.add(all_data)
        db.session.commit()
        logger.info(
            'Data saved successfully with record_id: %s',
            all_data.record_id)

        return
