from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from webapp.config import Config
from flask_bootstrap import Bootstrap
from flask_apscheduler import APScheduler

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = "You need to be logged in to view this page"
login_manager.login_message_category = "info"
mail = Mail()
scheduler = APScheduler()
scheduler.api_enabled = True


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bootstrap = Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()


    from webapp.users.routes import users_bp
    from webapp.posts.routes import posts_bp
    from webapp.main.routes import main_bp
    from webapp.crypto.routes import cryptos_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(cryptos_bp)

    return app
