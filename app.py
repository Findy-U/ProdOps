from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AllData(db.Model):
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.Text)
    project_card_id = db.Column(db.Text)
    project_card_node_id = db.Column(db.Text)
    project_card_note = db.Column(db.Text)
    creator_id = db.Column(db.Integer)
    creator_login = db.Column(db.Text)
    changes_note_from = db.Column(db.Text)
    previous_projects_v2_item_node_id_from = db.Column(db.Text)
    previous_projects_v2_item_node_id_to = db.Column(db.Text)


def process_webhook(data):
    try:
        action = data.get('action')
        if action == 'edited':
            projects_v2_item = data.get('projects_v2_item', {})
            creator = projects_v2_item.get('creator', {})

            mapped_data = {
                'action': action,
                'project_card_id': projects_v2_item.get('id'),
                'project_card_node_id': projects_v2_item.get('node_id'),
                'project_card_note': None,  # Set the appropriate values if needed
                'creator_id': creator.get('id') if creator else None,
                'creator_login': creator.get('login') if creator else None,
                'changes_note_from': None,  # Set the appropriate values if needed
                'previous_projects_v2_item_node_id_from': None,  # Set the appropriate values if needed
                'previous_projects_v2_item_node_id_to': None  # Set the appropriate values if needed
            }

            # Create a new AllData object and add it to the session
            all_data = AllData(**mapped_data)
            db.session.add(all_data)

            # Commit the session to save the changes to the database
            db.session.commit()

            logger.info('Data saved successfully')
        elif action == 'reordered':
            changes = data.get('changes', {})
            previous_projects_v2_item_node_id = changes.get('previous_projects_v2_item_node_id', {})

            mapped_data = {
                'action': action,
                'project_card_id': None,  # Set the appropriate values if needed
                'project_card_node_id': None,  # Set the appropriate values if needed
                'project_card_note': None,  # Set the appropriate values if needed
                'creator_id': None,  # Set the appropriate values if needed
                'creator_login': None,  # Set the appropriate values if needed
                'changes_note_from': None,  # Set the appropriate values if needed
                'previous_projects_v2_item_node_id_from': previous_projects_v2_item_node_id.get('from'),
                'previous_projects_v2_item_node_id_to': previous_projects_v2_item_node_id.get('to')
            }

            # Create a new AllData object and add it to the session
            all_data = AllData(**mapped_data)
            db.session.add(all_data)

            # Commit the session to save the changes to the database
            db.session.commit()

            logger.info('Data saved successfully')
        else:
            logger.info('Action is not "edited" or "reordered". Skipping webhook processing.')

    except Exception as e:
        logger.exception('An error occurred while processing the webhook: %s', str(e))
        db.session.rollback()

    return jsonify({'message': 'Webhook processed successfully'})

@app.route('/payload', methods=['POST'])
def webhook():
    data = request.get_json()
    if data is None:
        logger.error('Invalid JSON payload')
        abort(400)
    logger.info('Received webhook payload: %s', data)
    process_webhook(data)
    return jsonify({'message': 'Webhook processed successfully'})

if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database connected and tables created successfully.")
        except Exception as e:
            logger.error(f"Error setting up database: {e}", exc_info=True)
        app.run(host='0.0.0.0', port=4567)