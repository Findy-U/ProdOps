from datetime import datetime, timezone
from models.models import Alldata
from logger.logger import logger
from config import session

# Logger
logger = logger()


def process_webhook(data):
    try:
        logger.info('Type and value of data: %s, %s', type(data), data)
        action = data.get('action')

        if action in ['opened', 'reopened', 'assigned', 'closed', 'reordered', 'edited']:
            issue = data.get('issue')
            if issue:
                project_card_id = str(issue.get('id'))
                assignee = issue.get('assignee')
                if not assignee:
                    assignees = issue.get('assignees')
                    if assignees:
                        assignee = assignees[0]

                if assignee:
                    assignee_login = assignee.get(
                        'login') if assignee.get('login') else None

                created_at = issue.get('created_at')

                if created_at is not None:
                    created_at = datetime.strptime(
                        created_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

                closed_at = issue.get('closed_at')

                if closed_at is not None:
                    closed_at = datetime.strptime(
                        closed_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

                status = 'open' if closed_at is None else 'closed'

                existing_data = session.query(Alldata).filter_by(
                    project_card_id=project_card_id).first()

                if existing_data:
                    if assignee_login is not None:
                        existing_data.assignee = assignee_login
                    if closed_at is not None:
                        existing_data.closed_at = closed_at
                    if created_at is not None:
                        existing_data.created_at = created_at
                    if status is not None:
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
                    "Invalid payload structure. Skipping webhook processing.")
        else:
            logger.error(
                "Unsupported action: %s. Skipping webhook processing.", action)
    except Exception as e:
        logger.error("An error occurred during webhook processing: %s", str(e))
        session.rollback()
    finally:
        session.close()
