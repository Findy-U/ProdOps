from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from dotenv import load_dotenv
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ssl_args = {
    'ssl': {
        'ca': r'C:\Users\Ultra\Downloads\DigiCertGlobalRootCA.crt.pem'
    }
}

load_dotenv()

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'], connect_args=ssl_args)
Session = sessionmaker(bind=engine)

Base = declarative_base()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Alldata(Base):
    __tablename__ = 'alldata'

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    project_card_id = db.Column(db.Text)
    status = db.Column(db.Text)
    assignee = db.Column(db.Text)

def process_webhook(data):
    try:
        session = Session()
        logger.info('Type and value of data: %s, %s', type(data), data)
        action = data.get('action')

        if action in ['opened', 'reopened', 'assigned', 'closed', 'reordered', 'edited']:
            issue = data.get('issue')
            if issue:
                project_card_id = str(issue.get('id'))
                assignee = issue.get('assignee')
                if not assignee:
                    assignees = issue.get('assignees')
                    if assignees:
                        assignee = assignees[0]

                if assignee:
                    assignee_login = assignee.get('login')
                else:
                    assignee_login = None

                created_at = issue.get('created_at')
                if created_at is not None:
                    created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

                closed_at = issue.get('closed_at')
                if closed_at is not None:
                    closed_at = datetime.strptime(closed_at, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)

                status = 'open' if closed_at is None else 'closed'
                
                existing_data = session.query(Alldata).filter_by(project_card_id=project_card_id).first()

                if existing_data:
                    if assignee_login is not None:
                        existing_data.assignee = assignee_login
                    if closed_at is not None:
                        existing_data.closed_at = closed_at
                    if created_at is not None:
                        existing_data.created_at = created_at
                    if status is not None:
                        existing_data.status = status
                    try:
                        session.commit()
                        logger.info('Data updated successfully for record_id: %s', existing_data.record_id)
                    except Exception as e:
                        logger.error("An error occurred during updating data: %s", str(e))
                        session.rollback()
                else:
                    logger.info('No existing data found for project_card_id: %s', project_card_id)
                    all_data = Alldata(
                        project_card_id=project_card_id,
                        created_at=created_at,
                        closed_at=closed_at,
                        status=status,
                        assignee=assignee_login
                    )
                    session.add(all_data)
                    session.commit()
                    logger.info('Data saved successfully with record_id: %s', all_data.record_id)
            else:
                logger.error("Invalid payload structure. Skipping webhook processing.")
        else:
            logger.error("Unsupported action: %s. Skipping webhook processing.", action)
    except Exception as e:
        logger.error("An error occurred during webhook processing: %s", str(e))
        session.rollback()
    finally:
        session.close()


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

    app.run(host='0.0.0.0', port=4567)