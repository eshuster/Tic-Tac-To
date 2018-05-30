# # app/__init__.py

# from flask import Flask

# # Initialize the app
# app = Flask(__name__, instance_relative_config=True)

# # Load the views
# from app import views

# # Load the config file
# app.config.from_object('config')


# app/__init__.py

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # app = Flask(__name__, instance_relative_config=True)
    # print("****"* 10) 
    # print(app_config)
    # print("****"* 10)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    from app import models

    from .player import player as player_blueprint
    app.register_blueprint(player_blueprint, url_prefix='/player')
    
    from .board import board as board_blueprint
    app.register_blueprint(board_blueprint, url_prefix='/board')

    from .game import game as game_blueprint
    app.register_blueprint(game_blueprint, url_prefix='/game')

    # temporary route
    # @app.route('/')
    # def hello_world():
    #     return 'Hello, World!'

    return app

