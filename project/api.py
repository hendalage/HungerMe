from flask import Blueprint
from flask_restful import Api
from project.resources.users import UserCollection, LoginCollection
from project.resources.menus import MenuCollection, MenuItem

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
