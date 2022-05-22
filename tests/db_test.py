import os
import pytest
import tempfile
import time
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError
from project import create_app, db
from project.models.models import *



# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()


# based on http://flask.pocoo.org/docs/1.0/testing/
# we don't need a client for database testing, just the db handle
@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:1234@localhost/hm2",
        "TESTING": True
    }

    app = create_app(config)

    with app.app_context():
        db.create_all()

    yield app

    os.close(db_fd)
    os.unlink(db_fname)

# @pytest.fixture
# def db_handle(app):
#     db_fd, db_fname = tempfile.mkstemp()
#     app.app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost/hm2"
#     app.app.config["TESTING"] = True
#
#     with app.app.app_context():
#         app.db.create_all()
#
#     yield app.db
#
#     app.db.session.remove()
#     os.close(db_fd)
#     os.unlink(db_fname)

def _get_menu(restaurant_id="3a9e5c1a-acdb-450c-a85d-dfcaface1976"):
    return Menu(
        name='Pizza',
        description='Large chicken pizza',
        restaurant_id=restaurant_id,
        price=11.30,
        status=1
    )


def _get_restaurant():
    return Restaurant(
        name='City Restaurant',
        address='13 A, Rajakyla, Oulu',
        contact_no='+358402365487'
    )


def test_create_restaurant_menu(app):
    with app.app_context():
        restaurant = _get_restaurant()
        menu = _get_menu('3a9e5c1a-acdb-450c-a85d-dfcaface1976')
        menu.restaurant = restaurant
        db.session.add(restaurant)
        db.session.add(menu)
        db.session.commit()

        assert Restaurant.query.count() > 0
        assert Menu.query.count() > 1


def test_menu_ondelete(app):
    with app.app_context():
        menu = _get_menu('3a9e5c1a-acdb-450c-a85d-dfcaface1976')
        db.session.add(menu)
        db.session.commit()
        db.session.delete(menu)
        db.session.commit()
        assert menu is None
