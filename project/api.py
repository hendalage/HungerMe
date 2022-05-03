from flask import Blueprint
from flask_restful import Api
from project.resources.users import UserCollection, LoginCollection
from project.resources.menus import MenuCollection, MenuItem
from project.resources.orders import OrderCollection, OrderItem
from project.resources.inventory import InventoryCollection, InventoryItem
from project.resources.reservation import ReservationCollection, ReservationItem
from project.resources.restaurant import RestaurantCollection, RestaurantItem

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

# oder related resources
api.add_resource(OrderCollection, "/order/<uuid:restaurant_id>")
api.add_resource(OrderItem, "/oder/<uuid:restaurant_id>/<uuid:order_id>")

# Inventory related resources
api.add_resource(InventoryCollection, "/inventory/<uuid:restaurant_id>")
api.add_resource(InventoryItem, "/inventory/<uuid:restaurant_id>/<uuid:inventory_id>")

# Reservation related resources
api.add_resource(ReservationCollection, "/reservation/<uuid:restaurant_id>")
api.add_resource(ReservationItem, "/reservation/<uuid:restaurant_id>/<uuid:user_id>")

# Restaurant related resources
api.add_resource(RestaurantCollection, "/restaurant/")
api.add_resource(RestaurantItem, "/restaurant/<uuid:restaurant_id>")


