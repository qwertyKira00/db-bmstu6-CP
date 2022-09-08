from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore

import sys
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Database')
sys.path.insert(0, '/Users/anastasia/Desktop/ProgramEngineering/6Сем/DataBaseCP/FlaskApp/Backend')
import models, config

from config import Config

# init SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup Flask-Security
    from models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'main.authorization'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app