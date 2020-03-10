from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sendgrid import SendGridAPIClient
from bookingApp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

def splitChars(string):
    return [st for st in string]

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.jinja_env.filters['splitChars'] = splitChars

    db.init_app(app)
    bcrypt.init_app(app)

    from bookingApp.main.routes import main
    from bookingApp.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

app = create_app()