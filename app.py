from flask import Flask
from models.models import db, Base, Alldata
from logger.logger import logger
from config import engine
import os

from routes.webhook import webhook_route

# Logger
logger = logger()


def create_app(test: bool = False) -> Flask:
    app = Flask(__name__)

    if test:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Create a clone for testing
        Alldata.__tablename__ = 'alldata_test_clone'
        db.init_app(app)

        with app.app_context():
            Base.metadata.create_all(engine)

        return register_routes(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return register_routes(app)


def register_routes(app: Flask) -> Flask:
    app.register_blueprint(webhook_route)
    return app


# This var is declared for the sake of all imports through the app
app = create_app()


if __name__ == "__main__":
    with app.app_context():
        try:
            Base.metadata.create_all(engine)
            logger.info("Database connected and tables created successfully.")
        except Exception as e:
            logger.error(f"Error setting up database: {e}", exc_info=True)

    app.run(host='0.0.0.0', port=4567, debug=True)
