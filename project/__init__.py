"""
Init file
"""
import os
from flask import Flask
from flasgger import Swagger
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from project.constants import *

db = SQLAlchemy()
cache = Cache()


def create_app(test_config=None):
    """
    method to create application

    - Note reference to this method - course materials
        https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="postgresql://postgres:1234@localhost/hm2",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/hm2'

    app.config["SWAGGER"] = {
        "title": "HungerMe API",
        "openapi": "3.0.3",
        "uiversion": 3,
    }
    swagger = Swagger(app, template_file="doc/hungerme.yml")

    app.config["CACHE_TYPE"] = "FileSystemCache"
    app.config["CACHE_DIR"] = "cache"

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    cache.init_app(app)

    from project.converters import (
        UserConverter,
        MenuConverter,
        InventoryConverter,
        OrderConverter,
        RestaurantConverter
    )

    # Add converters
    app.url_map.converters["User"] = UserConverter
    app.url_map.converters["Menu"] = MenuConverter
    app.url_map.converters["Order"] = OrderConverter
    app.url_map.converters["Inventory"] = InventoryConverter
    app.url_map.converters["Restaurant"] = RestaurantConverter

    from project.dbutils import init_db_command
    from . import api

    app.cli.add_command(init_db_command)
    app.register_blueprint(api.api_bp)

    # @app.route('/hello', methods=['GET'])
    # def hello():
    #     return 'Hello, World!'

    return app


