from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from bookingApp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "info"

SGmail = SendGridAPIClient(Config.SENDGRID_API_KEY)

def splitChars(string):
    return [st for st in string]

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.jinja_env.filters['splitChars'] = splitChars

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from bookingApp.main.routes import main
    from bookingApp.admins.routes import admins
    from bookingApp.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(admins, url_prefix='/admin')
    app.register_blueprint(errors)

    return app

app = create_app()