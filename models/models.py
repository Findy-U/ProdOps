#O código acima define duas classes, Alldata e TestDB, que servem 
# como modelos para as tabelas 'alldata' e 'test_db' respectivamente, 
# em um banco de dados SQL. Ambas as classes usam a extensão 
# SQLAlchemy para Flask, que permite a interação com bancos de dados 
# SQL de uma maneira Pythonic.

#Cada classe tem cinco atributos, que representam as colunas na 
# respectiva tabela. Os atributos são record_id, created_at, 
# closed_at, project_card_id, status e assignee.

#O record_id é a chave primária, que é única para cada registro e 
# é incrementada automaticamente. created_at é a data e hora em que 
# o registro foi criado, que por padrão é o momento atual em UTC. 
# closed_at é a data e hora em que o registro foi fechado e pode ser 
# nulo. project_card_id é um identificador de texto para o cartão do 
# projeto, status é um campo de texto para o status e assignee é um 
# campo de texto para o responsável pela tarefa.

#Além disso, cada classe tem um construtor, que inicializa uma 
# instância da classe com os valores fornecidos para project_card_id, 
# status e assignee. Se ocorrer um erro durante a inicialização, o 
# erro é impresso.

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Cria uma instância do objeto SQLAlchemy, que será nosso manipulador 
# de banco de dados.
db = SQLAlchemy()

class Alldata(db.Model):
    """
    Classe Alldata define a estrutura da tabela 'alldata' em um banco 
    de dados. 

    Atributos:
    - record_id: Campo de número inteiro que serve como chave primária 
    para a tabela. É único para cada registro 
    e é incrementado automaticamente.
    - created_at: Campo do tipo data e hora que registra o momento em 
    que o registro foi criado. 
    Por padrão, é definido para o momento atual em UTC.
    - closed_at: Campo do tipo data e hora que registra o momento em 
    que o registro foi fechado. 
    Este campo pode ser nulo.
    - project_card_id: Campo de texto que serve como um identificador 
    para o cartão do projeto.
    - status: Campo de texto que armazena o status.
    - assignee: Campo de texto que armazena o responsável pela tarefa.
    """
    __tablename__ = 'alldata'
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    project_card_id = db.Column(db.Text)
    status = db.Column(db.Text)
    assignee = db.Column(db.Text)

    def __init__(self, project_card_id, status, assignee):
        """
        Construtor para a classe Alldata. 
        Ele inicializa uma instância da classe com os valores 
        fornecidos para project_card_id, status e assignee.
        Se ocorrer um erro durante a inicialização, o erro é impresso.
        """
        try:
            self.project_card_id = project_card_id
            self.status = status
            self.assignee = assignee
        except Exception as e:
            print("Erro ao criar uma nova instância Alldata:", e)


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

    def __init__(self, project_card_id, status, assignee):
        """
        Construtor para a classe TestDB. 
        Ele inicializa uma instância da classe com os valores 
        fornecidos para project_card_id, status e assignee.
        Se ocorrer um erro durante a inicialização, o erro é impresso.
        """
        try:
            self.project_card_id = project_card_id
            self.status = status
            self.assignee = assignee
        except Exception as e:
            print("Erro ao criar uma nova instância TestDB:", e)
