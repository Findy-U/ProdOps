from payload_example.full_payload_example import full_payload
from payload_example.issue_opened import issue_opened
from payload_example.issue_closed import issue_closed
from payload_example.issue_reopened import issue_reopened
from webhook.parse_issue import parse_issue

from models.models import db, TestDB

# Estes testes verificam a funcionalidade do webhook.

# Este teste verifica se a rota '/payload' retorna o código de status esperado (200) e a resposta correta ao receber o payload completo.
def test_send_payload_to_webhook(client) -> None:
    print("Enviando payload completo para a rota '/payload'...")
    response = client.post('/payload', json=full_payload)
    try:
        assert response.status_code == 200
        assert response.data == b'Must be the ping request'
        print("Teste passou com sucesso!")
    except AssertionError:
        print("Erro: Código de status ou resposta inesperada ao enviar payload completo!")

# Este teste verifica se a rota '/payload' retorna o código de status esperado (201) e a resposta correta ao receber um payload de issue aberta.
def test_issue_opened(client, app) -> None:
    print("Enviando payload de issue aberta para a rota '/payload'...")
    response = client.post('/payload', json=issue_opened)
    try:
        assert response.status_code == 201
        assert response.data == b'Resource created'
        print("Teste passou com sucesso!")
    except AssertionError:
        print("Erro: Código de status ou resposta inesperada ao enviar payload de issue aberta!")

# Este teste verifica se a rota '/payload' retorna o código de status esperado (204) ao receber um payload de issue fechada.
def test_issue_closed(client) -> None:
    print("Enviando payload de issue fechada para a rota '/payload'...")
    response = client.post('/payload', json=issue_closed)
    try:
        assert response.status_code == 204
        print("Teste passou com sucesso!")
    except AssertionError:
        print("Erro: Código de status inesperado ao enviar payload de issue fechada!")

# Este teste verifica se a rota '/payload' retorna o código de status esperado (204) ao receber um payload de issue reaberta.
def test_issue_reopened(client) -> None:
    print("Enviando payload de issue reaberta para a rota '/payload'...")
    response = client.post('/payload', json=issue_reopened)
    try:
        assert response.status_code == 204
        print("Teste passou com sucesso!")
    except AssertionError:
        print("Erro: Código de status inesperado ao enviar payload de issue reaberta!")

# Este teste verifica se os dados de uma issue aberta foram persistidos no banco de dados.
def test_verify_if_data_persisted(client, app) -> None:
    print("Verificando se os dados da issue aberta foram persistidos no banco de dados...")
    issue_parsed = parse_issue(issue_opened.get('issue'))

    with app.app_context():
        # Verifica se um registro com o id do cartão do projeto existe no banco de dados.
        check_record_exists = db.session.query(TestDB).filter_by(
            project_card_id=issue_parsed.get('project_card_id')).first()

        # A asserção verifica se o id do cartão do projeto no registro recuperado é igual ao id do cartão do projeto na issue aberta.
        try:
            assert check_record_exists.project_card_id == issue_parsed.get(
                'project_card_id')
            print("Teste passou com sucesso!")
        except AssertionError:
            print("Erro: Dados da issue aberta não foram persistidos no banco de dados corretamente!")
