from datetime import datetime, timezone


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
