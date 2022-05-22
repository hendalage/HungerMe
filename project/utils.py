from functools import wraps
import jwt
from flask import abort, request, jsonify
import json
from flask import Response, request, url_for
from project.constants import *
from project.models.models import *


def create_error_message(status_code, error, message=None):
    """
    Method to create error message
    Return
        - Error object
    """
    error_message = {
        'Code': status_code,
        'Error': error,
        'Message': message
    }
    return abort(status_code, error_message)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, 'thisissecret', algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['id']).first()
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated


class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href

    def add_control_post(self, ctrl_name, title, href, schema):
        """
        Utility method for adding POST type controls. The control is
        constructed from the method's parameters. Method and encoding are
        fixed to "POST" and "json" respectively.

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        : param str title: human-readable title for the control
        : param dict schema: a dictionary representing a valid JSON schema
        """

        self.add_control(
            ctrl_name,
            href,
            method="POST",
            encoding="json",
            title=title,
            schema=schema
        )

    def add_control_put(self, title, href, schema):
        """
        Utility method for adding PUT type controls. The control is
        constructed from the method's parameters. Control name, method and
        encoding are fixed to "edit", "PUT" and "json" respectively.

        : param str href: target URI for the control
        : param str title: human-readable title for the control
        : param dict schema: a dictionary representing a valid JSON schema
        """

        self.add_control(
            "edit",
            href,
            method="PUT",
            encoding="json",
            title=title,
            schema=schema
        )

    def add_control_delete(self, title, href):
        """
        Utility method for adding PUT type controls. The control is
        constructed from the method's parameters. Control method is fixed to
        "DELETE", and control's name is read from the class attribute
        *DELETE_RELATION* which needs to be overridden by the child class.

        : param str href: target URI for the control
        : param str title: human-readable title for the control
        """

        self.add_control(
            "mumeta:delete",
            href,
            method="DELETE",
            title=title,
        )


class HungerMeBuilder(MasonBuilder):

    # Collection controls
    def add_control_restaurants_all(self):
        self.add_control(
            "hungerme:restaurants-all",
            url_for("api.restaurantcollection"),
            title="All restaurants"
        )

    def add_control_reservations_all(self, restaurant):
        self.add_control(
            "hungerme:reservations-all",
            url_for("api.reservationcollection", restaurant=restaurant),
            title="All reservations"
        )

    def add_control_menus_all(self, restaurant):
        self.add_control(
            "hungerme:menus-all",
            url_for("api.menucollection", restaurant=restaurant),
            title="All menus"
        )

    def add_control_inventory_all(self, restaurant):
        self.add_control(
            "hungerme:inventory-all",
            url_for("api.inventorycollection", restaurant=restaurant),
            title="All inventory items"
        )

    def add_control_orders_all(self, restaurant):
        self.add_control(
            "hungerme:orders-all",
            url_for("api.ordercollection", restaurant=restaurant),
            title="All orders"
        )

    # Add controls
    def add_control_add_restaurant(self):
        self.add_control_post(
            "hungerme:add-restaurant",
            "Add a new restaurant",
            url_for("api.restaurantcollection"),
            Restaurant.get_schema()
        )

    def add_control_add_reservation(self, restaurant):
        self.add_control_post(
            "hungerme:add-reservation",
            "Add a new reservation",
            url_for("api.reservationcollection", restaurant=restaurant),
            Reservation.get_schema()
        )

    def add_control_add_menu(self, restaurant):
        self.add_control_post(
            "hungerme:add-menu",
            "Add a new menu",
            url_for("api.menucollection", restaurant=restaurant),
            Menu.get_schema()
        )

    def add_control_add_inventory(self, restaurant):
        self.add_control_post(
            "hungerme:add-inventory",
            "Add a new inventory item",
            url_for("api.inventorycollection", restaurant=restaurant),
            Inventory.get_schema()
        )

    def add_control_add_order(self, restaurant):
        self.add_control_post(
            "hungerme:add-order",
            "Add a new order",
            url_for("api.ordercollection", restaurant=restaurant),
            Order.get_schema()
        )

    # Delete controls
    def add_control_delete_restaurant(self, restaurant):
        self.add_control_delete(
            "Delete this restaurant",
            url_for("api.restaurantitem", restaurant=restaurant),
        )

    def add_control_delete_reservation(self, restaurant, user_id):
        self.add_control_delete(
            "Delete this reservation",
            url_for("api.reservationitem", restaurant=restaurant, user_id=user_id),
        )

    def add_control_delete_menu(self, restaurant, menu_id):
        self.add_control_delete(
            "Delete this menu",
            url_for("api.menuitem", restaurant=restaurant, menu_id=menu_id),
        )

    def add_control_delete_inventory(self, restaurant, inventory_id):
        self.add_control_delete(
            "Delete this inventory item",
            url_for("api.inventoryitem", restaurant=restaurant, inventory_id=inventory_id),
        )

    def add_control_delete_order(self, restaurant, order_id):
        self.add_control_delete(
            "Delete this order",
            url_for("api.orderitem", restaurant=restaurant, order_id=order_id),
        )

    # Edit controls
    def add_control_edit_restaurant(self, restaurant):
        self.add_control_put(
            "Edit this restaurant",
            url_for("api.restaurantitem", restaurant=restaurant),
            Restaurant.get_schema()
        )

    def add_control_edit_reservation(self, restaurant, user_id):
        self.add_control_put(
            "Edit this reservation",
            url_for("api.reservationitem", restaurant=restaurant, user_id=user_id),
            Reservation.get_schema()
        )

    def add_control_edit_menu(self, restaurant, menu_id):
        self.add_control_put(
            "Edit this menu",
            url_for("api.menuitem", restaurant=restaurant, menu_id=menu_id),
            Menu.get_schema()
        )

    def add_control_edit_inventory(self, restaurant, inventory_id):
        self.add_control_put(
            "Edit this inventory item",
            url_for("api.inventoryitem", restaurant=restaurant, inventory_id=inventory_id),
            Inventory.get_schema()
        )

    def add_control_edit_order(self, restaurant, order_id):
        self.add_control_put(
            "Edit this order",
            url_for("api.orderitem", restaurant=restaurant, order_id=order_id),
            Order.get_schema()
        )


def create_error_response(status_code, title, message=None):
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)


# def require_admin(func):
#     """
#     Method to validate admin key
#     """
#
#     def wrapper(*args, **kwargs):
#         api_key = request.headers.get("HRSystem-Api-Key")
#         if api_key is None:
#             return create_error_message(403, "Authentication Error")
#         key_hash = ApiKey.key_hash(
#             request.headers.get("HRSystem-Api-Key").strip())
#         db_key = ApiKey.query.filter_by(admin=True).first()
#         if secrets.compare_digest(key_hash, db_key.key):
#             return func(*args, **kwargs)
#         return create_error_message(403, "Authentication Error")
#     return wrapper


# def require_employee_key(func):
#     """
#     Method to validate employee key
#     """
#
#     def wrapper(self, employee, *args, **kwargs):
#         api_key = request.headers.get("HRSystem-Api-Key")
#         if api_key is None:
#             return create_error_message(403, "Authentication Error")
#         key_hash = ApiKey.key_hash(
#             request.headers.get("HRSystem-Api-Key").strip())
#         admin_db_key = ApiKey.query.filter_by(admin=True).first()
#         if secrets.compare_digest(key_hash, admin_db_key.key):
#             return func(self, employee, *args, **kwargs)
#         else:
#             db_key = ApiKey.query.filter_by(employee=employee).first()
#             if db_key is not None and secrets.compare_digest(
#                     key_hash, db_key.key):
#                 return func(self, employee, *args, **kwargs)
#             return create_error_message(403, "Authentication Error")
#
#     return wrapper
