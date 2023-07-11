from flask import request, abort, jsonify, Blueprint

from logger.logger import logger
from webhook.process_hook import process_webhook

logger = logger()
webhook_route = Blueprint('webhook', __name__)


@webhook_route.route('/payload', methods=['POST'])
def webhook():
    if not request.is_json:
        logger.error('Invalid JSON payload')
        abort(400)

    data = request.get_json()
    # logger.info('Received webhook payload: %s', data)
    process_webhook(data)

    return jsonify({'message': 'Webhook processed successfully'})
