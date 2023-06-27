from flask import Flask, jsonify, request, abort
import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from webhook.process_hook import process_webhook
from models.models import db, Base


load_dotenv()

ssl_args = {
    'ssl': {
        'ca': os.environ['SSL_PATH']
    }
}

DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

engine = create_engine(DATABASE_URI, connect_args=ssl_args)
Session = sessionmaker(bind=engine)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# App building
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/payload', methods=['POST'])
def webhook():
    if not request.is_json:
        logger.error('Invalid JSON payload')
        abort(400)
    data = request.get_json()
    logger.info('Received webhook payload: %s', data)
    process_webhook(data)
    return jsonify({'message': 'Webhook processed successfully'})


if __name__ == "__main__":
    with app.app_context():
        try:
            Base.metadata.create_all(engine)
            logger.info("Database connected and tables created successfully.")
        except Exception as e:
            logger.error(f"Error setting up database: {e}", exc_info=True)

    app.run(host='0.0.0.0', port=4567, debug=True)
