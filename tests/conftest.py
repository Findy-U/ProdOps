# O código é composto por três fixtures de teste criadas com a biblioteca
# pytest.

# A primeira fixture, app, é responsável por configurar o aplicativo no
# ambiente de teste, criar as tabelas necessárias no banco de dados e limpar
# o banco de dados após a execução de cada teste. Essa fixture tem escopo
# de sessão, o que significa que ela é executada uma vez por sessão de
# teste.

# A segunda fixture, client, é responsável por criar e retornar um cliente
# de teste que é usado para fazer solicitações ao aplicativo em um
# ambiente de teste. Esta fixture é chamada antes de cada teste que precisa
# de um cliente de teste.

# A terceira fixture, runner, é responsável por criar e retornar um runner
# de teste de linha de comando que é usado para executar comandos de linha
# de comando em um ambiente de teste. Esta fixture é chamada antes de cada
# teste que precisa de um runner CLI.

import pytest
from app import create_app
from models.models import TestDB, db


@pytest.fixture(scope='session')
def app():
    """
    Configura o estado do app para os testes. Esta fixture tem escopo de
    sessão, o que significa que é chamada apenas uma vez por sessão de teste.

    Antes de cada teste, essa fixture configura o app no modo de teste e cria
    todas as tabelas no banco de dados.

    Depois de cada teste, ela apaga todos os registros da tabela TestDB.

    Exceções que ocorrem durante a criação das tabelas ou a exclusão dos
    registros são tratadas e impressas.
    """
    print("Iniciando setup do app de teste...")
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.query(TestDB).delete()
        db.session.commit()


@pytest.fixture()
def client(app):
    """
    Configura e retorna um cliente de teste.

    O cliente de teste é usado para fazer solicitações ao app em um ambiente
    de teste. Essa fixture é chamada antes de cada teste que precisa de um
    cliente de teste.
    """
    return app.test_client()


@pytest.fixture()
def runner(app):
    """
    Configura e retorna um runner de teste de linha de comando (CLI).

    O runner CLI é usado para chamar comandos de linha de comando em um
    ambiente de teste. Essa fixture é chamada antes de cada teste que
    precisa de um runner CLI.
    """
    return app.test_cli_runner()
