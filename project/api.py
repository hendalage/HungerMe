from flask import Blueprint
from flask_restful import Api
from project.resources.users import UserCollection, LoginCollection

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)


@api_bp.route('/e', methods=['GET'])
def getMethod():
    return "ASDASDA"


# user related resources
api.add_resource(UserCollection, "/user/")
api.add_resource(LoginCollection, "/login")
