from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import requests
import http.client as http_client
http_client.HTTPConnection.debuglevel = 1

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AllData(db.Model):
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    project_card_id = db.Column(db.Text)
    status = db.Column(db.Text)
    assignee = db.Column(db.Text)  # New column for the assignee

def process_webhook(data):
    try:
        issue = data.get('issue')
        if issue:
            project_card_id = str(issue.get('id'))  # convert to string
            status = issue.get('state')

            # Get the assignee information
            assignee = issue.get('assignee')
            assignee_login = assignee.get('login') if assignee else None  # Handle case where assignee might be None

            created_at = datetime.strptime(issue.get('created_at'), "%Y-%m-%dT%H:%M:%SZ")
            closed_at = datetime.strptime(issue.get('closed_at'), "%Y-%m-%dT%H:%M:%SZ") if status == 'closed' else None

            # Check if the project_card_id already exists in the database
            existing_data = AllData.query.filter_by(project_card_id=project_card_id).first()

            if existing_data:
                # If the card already exists, update its status, closed_at date and assignee
                existing_data.status = status
                existing_data.closed_at = closed_at
                existing_data.created_at = created_at
                existing_data.assignee = assignee_login  # update assignee field
                logger.info('Data updated successfully for record_id: %s', existing_data.record_id)
            else:
                # If the card doesn't exist, create a new AllData object and add it to the session
                all_data = AllData(project_card_id=project_card_id, status=status, closed_at=closed_at, created_at=created_at, assignee=assignee_login)
                db.session.add(all_data)
                logger.info('Data saved successfully with record_id: %s', all_data.record_id)

            # Commit the session to save the changes
            db.session.commit()
        else:
            logger.error("Issue not found in payload. Skipping webhook processing.")
    except Exception as e:
        logger.error("An error occurred during webhook processing: %s", str(e))
        db.session.rollback()

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

