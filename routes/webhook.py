from flask import request, abort, Blueprint, Response

from logger.logger import logger
from webhook.process_hook import process_webhook

logger = logger()

webhook_route = Blueprint('webhook', __name__)


@webhook_route.route('/payload', methods=['POST'])
def webhook() -> Response:
    if not request.is_json:
        logger.error('Invalid JSON payload')
        abort(400)

    data = request.get_json()

    return process_webhook(data)
