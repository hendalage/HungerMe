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
api.add_resource(MenuCollection, "/menu/<restaurant:restaurant>/")
api.add_resource(MenuItem, "/menu/<restaurant:restaurant>/<uuid:menu_id>/")

# oder related resources
api.add_resource(OrderCollection, "/order/<restaurant:restaurant>/")
api.add_resource(OrderItem, "/order/<restaurant:restaurant>/<uuid:order_id>/")

# Inventory related resources
api.add_resource(InventoryCollection, "/inventory/<restaurant:restaurant>/")
api.add_resource(InventoryItem, "/inventory/<restaurant:restaurant>/<uuid:inventory_id>/")

# Reservation related resources
api.add_resource(ReservationCollection, "/reservation/<restaurant:restaurant>/")
api.add_resource(ReservationItem, "/reservation/<restaurant:restaurant>/<uuid:user_id>/")

# Restaurant related resources
api.add_resource(RestaurantCollection, "/restaurant/")
api.add_resource(RestaurantItem, "/restaurant/<restaurant:restaurant>/")


