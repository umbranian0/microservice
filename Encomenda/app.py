import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

logging.basicConfig(level=logging.DEBUG)

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    logging.debug("Initializing the database.")
    db.init_app(app)
    logging.debug("Initializing migration.")
    migrate.init_app(app, db)

    from routes import encomenda_blueprint
    app.register_blueprint(encomenda_blueprint)

    logging.debug("Blueprint registered successfully.")

    return app

if __name__ == '__main__':
    app = create_app()
    logging.debug("Starting the application.")
    app.run(debug=True, port=5003)

