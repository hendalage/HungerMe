from flask import Blueprint
from flask_restful import Api
from project.resources.users import UserCollection, LoginCollection
from project.resources.menus import MenuCollection, MenuItem
from project.resources.orders import OrderCollection, OrderItem
from project.resources.inventory import InventoryCollection, InventoryItem
from project.resources.reservation import ReservationCollection, ReservationItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)


@api_bp.route('/e', methods=['GET'])
def getMethod():
    return "ASDASDA"


# user related resources
api.add_resource(UserCollection, "/user/")
api.add_resource(LoginCollection, "/login")


# menu related resources
api.add_resource(MenuCollection, "/menu/list/<uuid:restaurant_id>")
api.add_resource(MenuItem, "/menu/new", "/menu/update/<string:menu_id>", "/menu/delete/<string:menu_id>", "/menu/get/<string:menu_id>")
# api.add_resource(MenuItem, "/menu/update/<string:menu_id>")
# api.add_resource(MenuItem, "/menu/delete/<string:menu_id>")
# api.add_resource(MenuItem, "/menu/get/<string:menu_id>")


# oder related resources
api.add_resource(OrderCollection, "/order/list/<uuid:restaurant_id>")
api.add_resource(OrderItem, "/order/new", "/oder/update/<string:order_id>", "/order/delete/<string:order_id>", "/order/get/<string:order_id>")

# Inventory related resources
api.add_resource(InventoryCollection, "/inventory/list/<uuid:restaurant_id>")
api.add_resource(InventoryItem, "/inventory/new", "/inventory/update/<string:inventory_id>", "/inventory/delete/<string:inventory_id>", "/inventory/get/<string:inventory_id>")

# Reservation related resources
api.add_resource(ReservationCollection, "/reservation/list/<uuid:restaurant_id>")
api.add_resource(ReservationItem, "/reservation/new", "/reservation/update/<string:reservation_id>", "/reservation/delete/<string:reservation_id>", "/reservation/get/<string:user_id>")

