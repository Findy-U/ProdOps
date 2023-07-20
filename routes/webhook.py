from flask import request, abort, Blueprint, Response

from logger.logger import logger
from webhook.process_hook import process_webhook

# Cria uma instância do logger.
logger = logger()
# Cria um blueprint chamado 'webhook'. Blueprints são uma maneira de organizar funcionalidades e rotas relacionadas 
# em aplicativos Flask.
webhook_route = Blueprint('webhook', __name__)

# Define a rota '/payload' no blueprint 'webhook'. Essa rota aceita apenas solicitações POST.
@webhook_route.route('/payload', methods=['POST'])
def webhook() -> Response:
    # Verifica se o payload da requisição é um JSON válido.
    if not request.is_json:
        # Se não for um JSON válido, loga uma mensagem de erro e retorna um erro 400 para o cliente.
        logger.error('Invalid JSON payload')
        abort(400)

    logger.info('Carregando dados da requisição...')
    # Caso seja um JSON válido, extrai os dados do payload.
    data = request.get_json()
    # Loga a informação dos dados recebidos na payload.
    logger.info('Dados da requisição carregados com sucesso. Processando webhook...')
    
    try:
        # Processa os dados recebidos e retorna a resposta.
        response = process_webhook(data)
        logger.info('Webhook processado com sucesso.')
        return response
    except Exception as e:
        logger.error(f'Erro ao processar webhook: {e}')
        abort(500)  # Retorna um erro 500 para o cliente, indicando que houve um erro no servidor.
