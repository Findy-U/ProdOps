from models.models import Alldata, TestDB
from logger.logger import logger
from .parse_issue import parse_issue
from models.models import db
from flask import current_app

# Criação do logger
logger = logger()

def process_webhook(data: dict) -> tuple:
    print("Iniciando o processamento do webhook...")
    # logger.info('Type and value of data: %s, %s', type(data), data)
    db_instance = Alldata

    if current_app.config["TESTING"]:
        db_instance = TestDB

    action = data.get('action')
    issue = data.get('issue')

    if not issue:
        logger.error(
            "Estrutura de payload inválida. Pulando o processamento do webhook.")
        db.session.close()

        return 'Deve ser a solicitação ping', 200

    parsed_issue = parse_issue(issue)

    if action == 'reopened':
        return issue_reopened(parsed_issue, db_instance)

    if action in ['opened', 'assigned', 'closed', 'reordered', 'edited']:
        return issue_create_or_edit(parsed_issue, db_instance)

    else:
        logger.error(
            "Ação não suportada: %s. Pulando o processamento do webhook.")

        return 'Ação não suportada', 400


def issue_reopened(parsed_issue: dict, db_instance) -> tuple:
    print("Processando issue reaberta...")
    project_card_id = parsed_issue['project_card_id']

    existing_data = db.session.query(db_instance).filter_by(
        project_card_id=project_card_id).first()

    existing_data.closed_at = None
    existing_data.status = 'Maintenance'

    db.session.add(existing_data)
    db.session.commit()
    logger.info(
        'Issue reaberta com sucesso para record_id: %s',
        existing_data.record_id)

    return '', 204


def issue_create_or_edit(parsed_issue: dict, db_instance) -> tuple:
    print("Processando criação ou edição de issue...")
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
            'Dados atualizados com sucesso para record_id: %s',
            existing_data.record_id)

        return '', 204

    else:
        logger.info(
            'Nenhum dado existente encontrado para project_card_id: %s',
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
            'Dados salvos com sucesso com record_id: %s',
            all_data.record_id)

        return 'Recurso criado', 201