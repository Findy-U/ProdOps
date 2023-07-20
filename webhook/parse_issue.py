from datetime import datetime, timezone

def parse_issue(issue: dict) -> dict:
    print("Iniciando o parsing da issue...")
    project_card_id = str(issue.get('id'))

    if not project_card_id:
        raise ValueError("Erro: 'id' da issue não encontrada.")
    
    assignee = issue.get('assignee')
    assignee_login = None

    if not assignee:
        assignees = issue.get('assignees')

        if assignees:
            assignee = assignees[0]
            login = assignee.get('login')
            assignee_login = login if login else None
        else:
            print("Aviso: Issue sem um 'assignee' atribuído.")
    
    created_at = issue.get('created_at')

    if created_at:
        print("Processando o campo 'created_at'...")
        created_at = datetime.strptime(
            created_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    else:
        raise ValueError("Erro: Campo 'created_at' não encontrado ou vazio na issue.")
    
    closed_at = issue.get('closed_at')

    if closed_at:
        print("Processando o campo 'closed_at'...")
        closed_at = datetime.strptime(
            closed_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    else:
        print("Aviso: Campo 'closed_at' não encontrado ou vazio na issue. A issue pode ainda estar aberta.")

    print("Parsing da issue concluído com sucesso.")
    return {
        "project_card_id": project_card_id,
        "assignee": assignee,
        "assignee_login": assignee_login,
        "created_at": created_at,
        "closed_at": closed_at
    }
