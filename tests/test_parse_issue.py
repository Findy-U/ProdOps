from payload_example.issue_example import issue
from webhook.parse_issue import parse_issue
import datetime

# Aqui estão sendo realizados testes para a função parse_issue.

# Este teste verifica se a função parse_issue retorna um dicionário.
def test_parse_issue_returns_dict() -> None:
    print("Iniciando teste: test_parse_issue_returns_dict...")
    try:
        # A função parse_issue é chamada com o argumento 'issue'.
        parsed_issue = parse_issue(issue)
        # A asserção verifica se o tipo do retorno é um dicionário.
        assert type(parsed_issue) is dict
        print("Teste finalizado com sucesso!")
    except AssertionError:
        print("Erro: A função parse_issue não retornou um dicionário!")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Este teste verifica se a função parse_issue retorna o dicionário esperado.
def test_parse_issue_returns_expected_dict() -> None:
    print("Iniciando teste: test_parse_issue_returns_expected_dict...")
    # Define o dicionário que é esperado como retorno da função.
    expected_return = {
        'project_card_id': '1793822382',
        'assignee': {
            'login': 'Demian143',
            'id': 81446007,
            'node_id': 'MDQ6VXNlcjgxNDQ2MDA3',
            'avatar_url': 'https://avatars.githubusercontent.com/u/81446007?v=4',
            'gravatar_id': '',
            'url': 'https://api.github.com/users/Demian143',
            'html_url': 'https://github.com/Demian143',
            'followers_url': 'https://api.github.com/users/Demian143/followers',
            'following_url': 'https://api.github.com/users/Demian143/following{/other_user}',
            'gists_url': 'https://api.github.com/users/Demian143/gists{/gist_id}',
            'starred_url': 'https://api.github.com/users/Demian143/starred{/owner}{/repo}',
            'subscriptions_url': 'https://api.github.com/users/Demian143/subscriptions',
            'organizations_url': 'https://api.github.com/users/Demian143/orgs',
            'repos_url': 'https://api.github.com/users/Demian143/repos',
            'events_url': 'https://api.github.com/users/Demian143/events{/privacy}',
            'received_events_url': 'https://api.github.com/users/Demian143/received_events',
            'type': 'User',
            'site_admin': False
        },
        'assignee_login': None,
        'created_at': datetime.datetime(2023, 7, 7, 16, 24, 5, tzinfo=datetime.timezone.utc),
        'closed_at': None
    }

    try:
        # A asserção verifica se o retorno da função parse_issue é igual ao dicionário esperado.
        assert parse_issue(issue) == expected_return
        print("Teste finalizado com sucesso!")
    except AssertionError:
        print("Erro: A função parse_issue não retornou o dicionário esperado!")
    except Exception as e:
        print(f"Erro inesperado: {e}")
