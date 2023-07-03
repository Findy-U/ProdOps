from datetime import datetime, timezone
from models.models import Alldata
from logger.logger import logger
from config import session as Session

# Logger
logger = logger()

session = Session()


def process_webhook(data: dict):
    try:
        logger.info('Type and value of data: %s, %s', type(data), data)
        action = data.get('action')
        issue = data.get('issue')

        if action == 'reopened':
            # 1 - Get object by id
            parsed_issue = parse_issue(issue)
            project_card_id = parsed_issue['project_card_id']

            existing_data = session.query(Alldata).filter_by(
                project_card_id=project_card_id).first()

            # 2 - Set closed_at to None and status to Open
            existing_data.closed_at = None
            existing_data.status = 'Open'

            session.add(existing_data)
            session.commit()
            logger.info(
                'Issue reopened successfully for record_id: %s',
                existing_data.record_id)
            # 3.1 - return response
            return

        if action in ['opened', 'assigned', 'closed', 'reordered', 'edited']:
            if not issue:
                logger.error(
                    "Invalid payload structure. Skipping webhook processing.")
                session.close()
                return

            parsed_issue = parse_issue(issue)

            closed_at = parsed_issue["closed_at"]
            project_card_id = parsed_issue["project_card_id"]
            assignee_login = parsed_issue["assignee_login"]
            created_at = parsed_issue["created_at"]

            status = 'open' if closed_at is None else 'closed'

            # Check if record is already in DB
            existing_data = session.query(Alldata).filter_by(
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

                try:
                    session.commit()
                    logger.info(
                        'Data updated successfully for record_id: %s', existing_data.record_id)

                except Exception as e:
                    logger.error(
                        "An error occurred during updating data: %s", str(e))
                    session.rollback()

            else:
                logger.info(
                    'No existing data found for project_card_id: %s', project_card_id)
                all_data = Alldata(
                    project_card_id=project_card_id,
                    created_at=created_at,
                    closed_at=closed_at,
                    status=status,
                    assignee=assignee_login
                )
                session.add(all_data)
                session.commit()
                logger.info(
                    'Data saved successfully with record_id: %s', all_data.record_id)

        else:
            logger.error(
                "Unsupported action: %s. Skipping webhook processing.", action)
    except Exception as e:
        logger.error("An error occurred during webhook processing: %s", str(e))
        session.rollback()
    finally:
        session.close()


def parse_issue(issue: dict) -> dict:
    """ This function separates the parsing of issue dictionary from
        the rest of the webhook code, making it easier to read. """

    project_card_id = str(issue.get('id'))
    assignee = issue.get('assignee')
    assignee_login = None

    if not assignee:
        assignees = issue.get('assignees')

        if assignees:
            assignee = assignees[0]
            login = assignee.get('login')
            assignee_login = login if login else None

    created_at = issue.get('created_at')

    if created_at:
        created_at = datetime.strptime(
            created_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

    closed_at = issue.get('closed_at')

    if closed_at:
        closed_at = datetime.strptime(
            closed_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

    return {
        "project_card_id": project_card_id,
        "assignee": assignee,
        "assignee_login": assignee_login,
        "created_at": created_at,
        "closed_at": closed_at
    }
