from flask import Blueprint
from flask_restful import Api
from project.resources.users import UserCollection, LoginCollection
from project.resources.menus import MenuCollection, MenuItem
from project.resources.oders import OderCollection, OderItem
from project.resources.inventory import InventoryCollection, InventoryItem

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
api.add_resource(OderCollection, "/oder/list/<uuid:restaurant_id>")
api.add_resource(OderItem, "/oder/new", "/oder/update/<string:oder_id>", "/oder/delete/<string:oder_id>", "/oder/get/<string:oder_id>")


# Inventory related resources
api.add_resource(InventoryCollection, "/inventory/list/<uuid:restaurant_id>")
api.add_resource(InventoryItem, "/inventory/list/<uuid:restaurant_id>")
