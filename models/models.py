# O código acima define duas classes, Alldata e TestDB, que servem
# como modelos para as tabelas 'alldata' e 'test_db' respectivamente,
# em um banco de dados SQL. Ambas as classes usam a extensão
# SQLAlchemy para Flask, que permite a interação com bancos de dados
# SQL de uma maneira Pythonic.

# Cada classe tem cinco atributos, que representam as colunas na
# respectiva tabela. Os atributos são record_id, created_at,
# closed_at, project_card_id, status e assignee.

# O record_id é a chave primária, que é única para cada registro e
# é incrementada automaticamente. created_at é a data e hora em que
# o registro foi criado, que por padrão é o momento atual em UTC.
# closed_at é a data e hora em que o registro foi fechado e pode ser
# nulo. project_card_id é um identificador de texto para o cartão do
# projeto, status é um campo de texto para o status e assignee é um
# campo de texto para o responsável pela tarefa.

# Além disso, cada classe tem um construtor, que inicializa uma
# instância da classe com os valores fornecidos para project_card_id,
# status e assignee. Se ocorrer um erro durante a inicialização, o
# erro é impresso.

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Alldata(db.Model):
    """ There's only one attribute in this class using nullable as true.
        It's good to notice that in DB all attributes are nullable except
        by record_key, that is the primary key. """

    __tablename__ = 'alldata'

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    project_card_id = db.Column(db.Text)
    status = db.Column(db.Text)
    assignee = db.Column(db.Text)


class TestDB(db.Model):
    """
    Classe TestDB define a estrutura da tabela 'test_db' em um banco
    de dados. Esta tabela não deve ser usada para testes.

    A estrutura da tabela 'test_db' é idêntica à estrutura da tabela
    'alldata'.
    """

    __test__ = False
    __tablename__ = 'test_db'

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    project_card_id = db.Column(db.Text)
    status = db.Column(db.Text)
    assignee = db.Column(db.Text)
