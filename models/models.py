from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Cria uma instância do objeto SQLAlchemy, que será nosso manipulador de banco de dados.
db = SQLAlchemy()

# Define a classe Alldata como um modelo para a tabela 'alldata' no banco de dados.
class Alldata(db.Model):
    __tablename__ = 'alldata'

    # Define a estrutura da tabela 'alldata'.
    # Cada atributo representa uma coluna na tabela.
    
    # record_id é a chave primária, que é única para cada registro e é incrementada automaticamente.
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # created_at é a data e hora em que o registro foi criado, e por padrão é o momento atual em UTC.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # closed_at é a data e hora em que o registro foi fechado. É permitido ser nulo.
    closed_at = db.Column(db.DateTime, nullable=True)
    # project_card_id é um identificador de texto para o cartão do projeto.
    project_card_id = db.Column(db.Text)
    # status é um campo de texto para o status.
    status = db.Column(db.Text)
    # assignee é um campo de texto para o responsável pela tarefa.
    assignee = db.Column(db.Text)

    # Adicionando um construtor para melhor manipulação de erros.
    def __init__(self, project_card_id, status, assignee):
        try:
            self.project_card_id = project_card_id
            self.status = status
            self.assignee = assignee
        except Exception as e:
            print("Erro ao criar uma nova instância Alldata:", e)

# Define a classe TestDB como um modelo para a tabela 'test_db' no banco de dados.
# __test__ é definido como False, indicando que essa tabela não deve ser usada para testes.
class TestDB(db.Model):
    __test__ = False
    __tablename__ = 'test_db'

    # A estrutura da tabela 'test_db' é idêntica à estrutura da tabela 'alldata'.
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    project_card_id = db.Column(db.Text)
    status = db.Column(db.Text)
    assignee = db.Column(db.Text)

    # Adicionando um construtor para melhor manipulação de erros.
    def __init__(self, project_card_id, status, assignee):
        try:
            self.project_card_id = project_card_id
            self.status = status
            self.assignee = assignee
        except Exception as e:
            print("Erro ao criar uma nova instância TestDB:", e)
