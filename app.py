from flask import Flask
from models.models import db
from logger.logger import logger
import dotenv
import os

from routes.webhook import webhook_route

# Inicializando o logger
logger = logger()

def create_app() -> Flask:
    print("Criando aplicação...")
    # Carregando todas as variáveis de ambiente
    dotenv.load_dotenv('.env')

    app = Flask(__name__)

    # Configurando a URI do banco de dados SQLAlchemy e desativando o rastreamento de modificações
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializando o banco de dados com o app
    db.init_app(app)
    register_routes(app)

    print("Aplicação criada com sucesso...")
    return app

def register_routes(app: Flask) -> Flask:
    print("Registrando rotas...")
    app.register_blueprint(webhook_route)
    print("Rotas registradas com sucesso...")
    return app

# Criando a aplicação
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        try:
            print("Configurando o banco de dados...")
            db.create_all()
            logger.info("Conexão com o banco de dados estabelecida e tabelas criadas com sucesso.")
            print("Banco de dados configurado com sucesso...")
        except Exception as e:
            logger.error(f"Erro ao configurar o banco de dados: {e}", exc_info=True)

    # Rodando a aplicação
    app.run(host='0.0.0.0', port=4567, debug=True)
