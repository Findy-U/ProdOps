from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ssl_args = {
    'ssl': {
        'ca': r'C:\Users\cesar\Documents\Projetos\Findy\DigiCertGlobalRootCA.crt.pem'
    }
}

load_dotenv()

engine = create_engine(
    os.environ['SQLALCHEMY_DATABASE_URI'], connect_args=ssl_args)
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
        issue = data.get('issue')
        if issue:
            project_card_id = str(issue.get('id'))
            status = issue.get('state')

            # Get the assignee information
            assignee = issue.get('assignee')
            assignee_login = assignee.get('login') if assignee else None
            # Add this line for debugging
            logger.info('Assignee login: %s', assignee_login)

            created_at = datetime.strptime(
                issue.get('created_at'), "%Y-%m-%dT%H:%M:%SZ")
            closed_at = datetime.strptime(
                issue.get('closed_at'), "%Y-%m-%dT%H:%M:%SZ") if status == 'closed' else None

            existing_data = session.query(Alldata).filter_by(
                project_card_id=project_card_id).first()

            if existing_data:
                # If the card already exists, update its status, closed_at date, and assignee
                existing_data.status = status
                existing_data.closed_at = closed_at
                existing_data.created_at = created_at
                existing_data.assignee = assignee_login
                logger.info(
                    'Data updated successfully for record_id: %s', existing_data.record_id)
            else:
                all_data = Alldata(
                    project_card_id=project_card_id,
                    status=status,
                    closed_at=closed_at,
                    created_at=created_at,
                    assignee=assignee_login
                )
                logger.info('Assignee value before saving: %s',
                            all_data.assignee)  # Add this line for debugging
                session.add(all_data)
                logger.info(
                    'Data saved successfully with record_id: %s', all_data.record_id)

            # Commit the session to save the changes
            session.commit()
        else:
            logger.error(
                "Issue not found in payload. Skipping webhook processing.")
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
