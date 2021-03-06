from flask import Flask

from .extensions import db, login_manager

def create_app(config_file= "setting.py"):
    app = Flask (__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)
    
    login_manager.init_app(app)

    # login_manager.login_view = ""

    # @login_manager.user_loader
    #def load_user(user_id):
    #   return User.query.get(user.id)

    return app
