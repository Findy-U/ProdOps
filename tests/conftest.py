import pytest
from app import create_app
from models.models import TestDB, db

# Fixtures são funções que são executadas pelo pytest antes de cada teste. 
# Elas são usadas para configurar um estado específico para os testes.

# Essa fixture chamada 'app' tem escopo de sessão, o que significa que é chamada apenas uma vez por sessão de teste.
@pytest.fixture(scope='session')
def app():
    print("Iniciando setup do app de teste...")
    # Setup
    # Cria uma instância do app e configura para o modo de teste.
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    try:
        # Cria todas as tabelas no banco de dados especificado na configuração do app.
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(f"Erro ao criar tabelas no banco de dados: {e}")

    print("Setup do app de teste finalizado. Executando testes...")
    # A instrução 'yield' é usada para permitir que o código de teste seja executado.
    # Após a execução do teste, o código após 'yield' é executado.
    yield app

    print("Iniciando teardown do app de teste...")
    # Teardown
    # Apaga todos os registros da tabela TestDB após a execução do teste.
    try:
        with app.app_context():
            db.session.query(TestDB).delete()
            db.session.commit()
    except Exception as e:
        print(f"Erro ao deletar registros da tabela TestDB: {e}")
    print("Teardown do app de teste finalizado.")

# Essa fixture cria um cliente de teste. 
# O cliente de teste é usado para fazer solicitações ao app em um ambiente de teste.
@pytest.fixture()
def client(app):
    print("Criando cliente de teste...")
    return app.test_client()

# Essa fixture cria um runner de teste de linha de comando (CLI). 
# O runner CLI é usado para chamar comandos de linha de comando em um ambiente de teste.
@pytest.fixture()
def runner(app):
    print("Criando runner de teste de linha de comando...")
    return app.test_cli_runner()