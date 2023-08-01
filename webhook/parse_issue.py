from datetime import datetime, timezone


def parse_issue(issue: dict) -> dict:
    """ This function separates the parsing of issue dictionary from
        the rest of the webhook code, making it easier to read. """

    project_card_id = str(issue.get('id'))
    assignee = issue.get('assignee')
    assignee_login = None

    # Se não houver um responsável, procura na lista de responsáveis.
    if not assignee:
        assignees = issue.get('assignees')

        if assignees:
            assignee = assignees[0]
            login = assignee.get('login')
            assignee_login = login if login else None

    closed_at = issue.get('closed_at')

    if closed_at:
        closed_at = datetime.strptime(
            closed_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

    repository_url = issue.get('repository_url')

    created_at = datetime.strptime(
        issue.get('created_at'),
        '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

    return {
        "project_card_id": project_card_id,
        "assignee": assignee,
        "assignee_login": assignee_login,
        "created_at": created_at,
        "closed_at": closed_at,
        "repository_url": repository_url
    }
