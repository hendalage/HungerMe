"""
This file contains the Converter methods
"""
from werkzeug.routing import BaseConverter
from project.models.models import User, Menu, Inventory, Reservation, Order, Restaurant
from project.utils import create_error_message
from project import db
from flask import make_response


class UserConverter(BaseConverter):
    """
    Converter for user entity in URL parameter
    """

    def to_python(self, user_id):
        """
        convert to a user object
        """
        role = db.session.query(User).filter_by(id=user_id).first()
        if role is None:
            return create_error_message(
                404, "Not found",
                "User not found"
            )
        return role

    def to_url(self, db_user):
        """
        return user id
        """
        return str(db_user.id)


# class MenuConverter(BaseConverter):
#     """
#     Converter for Menu entity in URL parameter
#     """
#
#     def to_python(self, menu_name):
#         """
#         convert to a menu object
#         """
#         menu = Menu.query.filter_by(name=menu_name).first()
#         if menu is None:
#             return create_error_message(
#                 404, "Not found",
#                 "Menu not found"
#             )
#         return menu
#
#     def to_url(self, db_menu):
#         """
#         return menu id
#         """
#         return str(db_menu.name)


class OrderConverter(BaseConverter):
    """
    Converter for order entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to an order object
        """
        role = Order.query.filter_by(id=value).first()
        if role is None:
            return create_error_message(
                404, "Not found",
                "User not found"
            )
        return role

    def to_url(self, value):
        """
        return order id
        """
        return str(value.id)


# class InventoryConverter(BaseConverter):
#     """
#     Converter for inventory entity in URL parameter
#     """
#
#     def to_python(self, inventory_id):
#         """
#         convert to an inventory object
#         """
#         try:
#             inventory_item = db.session.query(Inventory).filter_by(name=inventory_id).first()
#         except:
#             return make_response('Could not find menu item', 400, {'message': 'Please check your entries!"'})
#
#         if inventory_item is None:
#             return create_error_message(
#                 404, "Not found",
#                 "Menu not found"
#             )
#         return inventory_item

    def to_url(self, db_inventory):
        """
        return inventory id
        """
        return str(db_inventory.id)


class ReservationConverter(BaseConverter):
    """
    Converter for inventory entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to a reservation object
        """
        reservation = Reservation.query.filter_by(id=value).first()
        if reservation is None:
            return create_error_message(
                404, "Not found",
                "Menu not found"
            )
        return reservation

    def to_url(self, value):
        """
        return reservation id
        """
        return str(value.id)

class RestaurantConverter(BaseConverter):
    """
    Converter for restaurant entity in URL parameter
    """

    def to_python(self, restaurant_name):
        """
        convert to a restaurant object
        """
        # restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
        restaurant = db.session.query(Restaurant).filter_by(name=restaurant_name).first()
        if restaurant is None:
            return create_error_message(
                404, "Not found",
                "Restaurant not found"
            )
        return restaurant

    def to_url(self, db_restaurant):
        """
        return restaurant name
        """
        return db_restaurant.name

