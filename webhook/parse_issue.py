# Este código define uma função, parse_issue(), que analisa uma "issue"
# (problema) de um sistema de gerenciamento de projetos. A função
# recebe um dicionário representando a "issue" como entrada e retorna
# um novo dicionário contendo informações analisadas da "issue",
# incluindo o ID do projeto, o responsável, a data de criação e a data
# de encerramento.

# Durante a análise, o código também verifica se certos campos estão
# presentes na "issue". Se um campo necessário (como o ID da "issue"
# ou a data de criação) estiver ausente, a função levanta uma exceção.
# Se um campo opcional (como o responsável ou a data de fechamento)
# estiver ausente, a função simplesmente emite um aviso e continua.

from datetime import datetime, timezone


def parse_issue(issue: dict) -> dict:
    """
    Função para analisar uma 'issue'. A análise envolve extrair
    informações relevantes da issue,
    incluindo o ID do projeto, o responsável, a data de criação e a
    data de encerramento.

    :param issue: Dicionário que representa uma issue.
    :return: Dicionário contendo as informações analisadas.
    """

    project_card_id = str(issue.get('id'))  # ID do cartão do projeto.

    assignee = issue.get('assignee')  # Responsável pela issue.
    assignee_login = None  # Login do responsável.

    # Se não houver um responsável, procura na lista de responsáveis.
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

    # Retorna o dicionário com as informações analisadas.
    return {
        "project_card_id": project_card_id,
        "assignee": assignee,
        "assignee_login": assignee_login,
        "created_at": created_at,
        "closed_at": closed_at
    }
