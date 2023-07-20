#O código define uma rota chamada '/payload' que aceita solicitações 
# POST. Ela faz parte do blueprint 'webhook', que é uma forma de organizar 
# funcionalidades e rotas relacionadas em aplicativos Flask. A rota 
# '/payload' é projetada para processar payloads JSON.

#Quando uma solicitação é recebida, o código verifica se o payload é um 
# JSON válido. Se não for, uma mensagem de erro é registrada e um erro HTTP 
# 400 é retornado para o cliente.

#Se o payload for um JSON válido, o código extrai os dados do payload e tenta 
# processá-los. Durante esse processo, várias mensagens de log são 
# registradas para ajudar a monitorar o progresso do processamento.

#Se o processamento do payload for bem-sucedido, uma mensagem de sucesso é 
# registrada e a resposta é retornada para o cliente. No entanto, se ocorrer 
# um erro durante o processamento, uma mensagem de erro é registrada e um 
# erro HTTP 500 é retornado para o cliente.

from flask import request, abort, Blueprint, Response

from logger.logger import logger
from webhook.process_hook import process_webhook

# Cria uma instância do logger.
logger = logger()

# Cria um blueprint chamado 'webhook'. Blueprints são uma maneira de organizar 
# funcionalidades e rotas relacionadas 
# em aplicativos Flask.
webhook_route = Blueprint('webhook', __name__)

@webhook_route.route('/payload', methods=['POST'])
def webhook() -> Response:
    """
    Esta é uma rota '/payload' que aceita apenas solicitações POST. Essa rota 
    faz parte do blueprint 'webhook'.

    A rota recebe um payload JSON, verifica se o payload é válido e, em 
    seguida, o processa. 
    As mensagens de log são registradas em todas as etapas do processo.

    Se o payload não for um JSON válido, registra uma mensagem de erro e retorna 
    um erro 400 para o cliente.

    Se ocorrer um erro durante o processamento do payload, registra uma mensagem 
    de erro e retorna um erro 500 para o cliente.

    Se o payload for processado com sucesso, registra uma mensagem de sucesso e 
    retorna a resposta para o cliente.
    """
    if not request.is_json:
        logger.error('Invalid JSON payload')
        abort(400)

    logger.info('Carregando dados da requisição...')
    data = request.get_json()
    logger.info('Dados da requisição carregados com sucesso. Processando webhook...')
    
    try:
        response = process_webhook(data)
        logger.info('Webhook processado com sucesso.')
        return response
    except Exception as e:
        logger.error(f'Erro ao processar webhook: {e}')
        abort(500)
