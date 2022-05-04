from email import header
import json
import os
import secrets
import pytest
import tempfile

from project import create_app, db
from project.models.models import *




@pytest.fixture
def client():
    """ This method create the client , database and configurations
    """
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:1234@localhost/hm1",
        "TESTING": True
    }

    app = create_app(config)

    with app.app_context():
        db.create_all()
        _populate_db()

    yield app.test_client()

    os.close(db_fd)
    os.unlink(db_fname)


def _populate_db():
    restaurant = Restaurant(
        name='Linnanmaa Restaurant',
        address='20 A, Oulu',
        contact_no="+358404569865"
    )
    db.session.add(restaurant)

    menu = Menu(name="Pizza Menu0", description="Large Pizza slices",
                restaurant_id="3a9e5c1a-acdb-450c-a85d-dfcaface1976", price=12.00,
                status=1)
    db.session.add(menu)

    order = Order(user_id="49b9deb3-0258-405f-ac0f-6382a7994664", restaurant_id="3a9e5c1a-acdb-450c-a85d-dfcaface1976",
                  menu_id="bd57ff87-e9e4-4b59-a386-b3193b9e29b9", qty=22, status=1)
    db.session.add(order)

    db.session.commit()


def _get_menu_json(restaurant_id="3a9e5c1a-acdb-450c-a85d-dfcaface1976"):
    return {"name": "Pizza Menu1", "description": "Large Pizza slices", "restaurant_id": restaurant_id, "price": 11.30,
            "status": 1}


def _get_menu_put_json(menu_id="bd57ff87-e9e4-4b59-a386-b3193b9e29b9"):
    return {"menu_id": menu_id, "name": "Pizza Menu1", "description": "Large Pizza slices", "price": 11.30,
            "status": 1}


def _get_order_json(order_id="211b0687-2956-40e1-abc2-10c5ae00258a"):
    return {"order_id": order_id, "user_id": "49b9deb3-0258-405f-ac0f-6382a7994664",
            "restaurant_id": "3a9e5c1a-acdb-450c-a85d-dfcaface1976",
            "menu_id": "bd57ff87-e9e4-4b59-a386-b3193b9e29b9", "quantity": 22,
            "status": 1}


def _get_order_put_json(order_id="211b0687-2956-40e1-abc2-10c5ae00258a"):
    return {"user_id": "49b9deb3-0258-405f-ac0f-6382a7994664", "restaurant_id": "3a9e5c1a-acdb-450c-a85d-dfcaface1976",
            "menu_id": "2a31bf85-e61d-4fd0-8bfa-b676bc14fe50", "quantity": 22,
            "status": 1}


class TestMenuCollection(object):
    RESOURCE_URL = "/api/menu/3a9e5c1a-acdb-450c-a85d-dfcaface1976"

    def test_get(self, client):
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 200
        body = json.loads(res.data)
        assert len(body) > 0


class TestOrderCollection(object):
    RESOURCE_URL = "/api/order/3a9e5c1a-acdb-450c-a85d-dfcaface1976"

    def test_get(self, client):
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 200
        body = json.loads(res.data)
        assert len(body) > 0


class TestMenuItem(object):
    RESOURCE_URL = "/api/menu/"

    def test_get(self, client):
        res = client.get(
            self.RESOURCE_URL + '3a9e5c1a-acdb-450c-a85d-dfcaface1976/bd57ff87-e9e4-4b59-a386-b3193b9e29b9')
        assert res.status_code == 200
        body = json.loads(res.data)

    def test_post(self, client):
        menu = _get_menu_json()
        res = client.post(self.RESOURCE_URL + '3a9e5c1a-acdb-450c-a85d-dfcaface1976', data=json.dumps(menu))
        assert res.status_code == 200

    def test_put(self, client):
        menu = _get_menu_put_json()
        res = client.post(
            self.RESOURCE_URL + '3a9e5c1a-acdb-450c-a85d-dfcaface1976/bd57ff87-e9e4-4b59-a386-b3193b9e29b9',
            data=json.dumps(menu))
        assert res.status_code == 201

    def test_delete(self, client):
        res = client.post(
            self.RESOURCE_URL + '3a9e5c1a-acdb-450c-a85d-dfcaface1976/bd57ff87-e9e4-4b59-a386-b3193b9e29b9')
        assert res.status_code == 204


class TestOderItem(object):
    RESOURCE_URL = "/api/order/"

    def test_get(self, client):
        res = client.get(
            self.RESOURCE_URL + '3a9e5c1a-acdb-450c-a85d-dfcaface1976/2e811150-31fc-47fe-9b5c-cc3ad4a8d590')
        assert res.status_code == 200
        body = json.loads(res.data)

    def test_post(self, client):
        order = _get_menu_json()
        res = client.post(self.RESOURCE_URL + '3a9e5c1a-acdb-450c-a85d-dfcaface1976', data=json.dumps(order))
        assert res.status_code == 200

    def test_put(self, client):
        order = _get_menu_put_json()
        res = client.post(
            self.RESOURCE_URL + '3a9e5c1a-acdb-450c-a85d-dfcaface1976/2e811150-31fc-47fe-9b5c-cc3ad4a8d590',
            data=json.dumps(order))
        assert res.status_code == 201

    def test_delete(self, client):
        res = client.post(
            self.RESOURCE_URL + '3a9e5c1a-acdb-450c-a85d-dfcaface1976/2e811150-31fc-47fe-9b5c-cc3ad4a8d590')
        assert res.status_code == 204
