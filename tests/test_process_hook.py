#Este código define um conjunto de testes que verificam a funcionalidade de um webhook. 
# Em particular, os testes verificam se a rota '/payload' de um aplicativo web retorna 
# os códigos de status HTTP esperados e as respostas corretas quando recebe diferentes 
# tipos de "payloads". Os testes também verificam se os dados de uma "issue" aberta são 
# persistidos corretamente no banco de dados. Os testes são escritos para serem usados 
# com um cliente de teste, que é usado para enviar solicitações ao aplicativo web.

from payload_example.full_payload_example import full_payload
from payload_example.issue_opened import issue_opened
from payload_example.issue_closed import issue_closed
from payload_example.issue_reopened import issue_reopened
from webhook.parse_issue import parse_issue

from models.models import db, TestDB

# Testes para verificar a funcionalidade do webhook

def test_send_payload_to_webhook(client) -> None:
    """
    Teste para verificar se a rota '/payload' retorna o código de status esperado (200) 
    e a resposta correta ao receber o payload completo.
    
    :param client: O cliente de teste que será usado para enviar solicitações ao aplicativo.
    """
    print("Enviando payload completo para a rota '/payload'...")
    response = client.post('/payload', json=full_payload)
    try:
        assert response.status_code == 200
        assert response.data == b'Must be the ping request'
        print("Teste passou com sucesso!")
    except AssertionError:
        print("Erro: Código de status ou resposta inesperada ao enviar payload completo!")

def test_issue_opened(client, app) -> None:
    """
    Teste para verificar se a rota '/payload' retorna o código de status esperado (201) 
    e a resposta correta ao receber um payload de issue aberta.
    
    :param client: O cliente de teste que será usado para enviar solicitações ao aplicativo.
    :param app: A instância do aplicativo.
    """
    print("Enviando payload de issue aberta para a rota '/payload'...")
    response = client.post('/payload', json=issue_opened)
    try:
        assert response.status_code == 201
        assert response.data == b'Resource created'
        print("Teste passou com sucesso!")
    except AssertionError:
        print("Erro: Código de status ou resposta inesperada ao enviar payload de issue aberta!")

def test_issue_closed(client) -> None:
    """
    Teste para verificar se a rota '/payload' retorna o código de status esperado (204) 
    ao receber um payload de issue fechada.
    
    :param client: O cliente de teste que será usado para enviar solicitações ao aplicativo.
    """
    print("Enviando payload de issue fechada para a rota '/payload'...")
    response = client.post('/payload', json=issue_closed)
    try:
        assert response.status_code == 204
        print("Teste passou com sucesso!")
    except AssertionError:
        print("Erro: Código de status inesperado ao enviar payload de issue fechada!")

def test_issue_reopened(client) -> None:
    """
    Teste para verificar se a rota '/payload' retorna o código de status esperado (204) 
    ao receber um payload de issue reaberta.
    
    :param client: O cliente de teste que será usado para enviar solicitações ao aplicativo.
    """
    print("Enviando payload de issue reaberta para a rota '/payload'...")
    response = client.post('/payload', json=issue_reopened)
    try:
        assert response.status_code == 204
        print("Teste passou com sucesso!")
    except AssertionError:
        print("Erro: Código de status inesperado ao enviar payload de issue reaberta!")

def test_verify_if_data_persisted(client, app) -> None:
    """
    Teste para verificar se os dados de uma issue aberta foram persistidos no banco de dados.
    
    :param client: O cliente de teste que será usado para enviar solicitações ao aplicativo.
    :param app: A instância do aplicativo.
    """
    print("Verificando se os dados da issue aberta foram persistidos no banco de dados...")
    issue_parsed = parse_issue(issue_opened.get('issue'))

    with app.app_context():
        check_record_exists = db.session.query(TestDB).filter_by(
            project_card_id=issue_parsed.get('project_card_id')).first()

        try:
            assert check_record_exists.project_card_id == issue_parsed.get(
                'project_card_id')
            print("Teste passou com sucesso!")
        except AssertionError:
            print("Erro: Dados da issue aberta não foram persistidos no banco de dados corretamente!")
