"""
This file contains the Converter methods
"""
from werkzeug.routing import BaseConverter
from project.models.models import User, Menu, Inventory, Reservation, Order, Restaurant
from project.utils import create_error_message


class UserConverter(BaseConverter):
    """
    Converter for user entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to a user object
        """
        role = User.query.filter_by(id=value).first()
        if role is None:
            return create_error_message(
                404, "Not found",
                "User not found"
            )
        return role

    def to_url(self, value):
        """
        return user id
        """
        return str(value.id)


class MenuConverter(BaseConverter):
    """
    Converter for Menu entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to a menu object
        """
        menu = Menu.query.filter_by(id=value).first()
        if menu is None:
            return create_error_message(
                404, "Not found",
                "Menu not found"
            )
        return menu

    def to_url(self, value):
        """
        return menu id
        """
        return str(value.id)


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


class InventoryConverter(BaseConverter):
    """
    Converter for inventory entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to an inventory object
        """
        inventory_item = Inventory.query.filter_by(id=value).first()
        if inventory_item is None:
            return create_error_message(
                404, "Not found",
                "Menu not found"
            )
        return inventory_item

    def to_url(self, value):
        """
        return inventory id
        """
        return str(value.id)


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

    def to_python(self, value):
        """
        convert to a restaurant object
        """
        restaurant = Restaurant.query.filter_by(id=value).first()
        if restaurant is None:
            return create_error_message(
                404, "Not found",
                "Menu not found"
            )
        return restaurant

    def to_url(self, value):
        """
        return restaurant id
        """
        return str(value.id)

