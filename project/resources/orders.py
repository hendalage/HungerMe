from flask import Response, request, jsonify, make_response
from project.utils import create_error_message, token_required
from project.models.models import Restaurant, User, Order, Menu
from project import db
from jsonschema import validate, ValidationError
from flask_restful import Resource


class OrderCollection(Resource):

    @classmethod
    # @token_required
    def get(cls, restaurant_id):
        orders = Order.query.filter_by(restaurant_id=restaurant_id).all()
        order_list = []
        print(orders)
        for order in orders:
            order_data = {
                'id': order.id,
                'user_id': order.user_id,
                'restaurant_id': order.restaurant_id,
                'status': order.status,
                'restaurant_name': order.restaurant.name,
                'restaurant_address': order.restaurant.address,
                'restaurant_contact_no': order.restaurant.contact_no,
                'menu_name': order.menu.name,
                'qty': order.qty,
                'menu_description': order.menu.description
            }
            order_list.append(order_data)

        return jsonify({'orders': order_list})

    @classmethod
    # @token_required
    def post(cls, restaurant_id):

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Order.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            data = request.get_json()

            new_order = Order(
                user_id=data['user_id'],
                restaurant_id=str(restaurant_id),
                menu_id=data['menu_id'],
                qty=data['qty'],
                status=data['status']
            )

            db.session.add(new_order)
            db.session.commit()

            return jsonify({'message': 'New order added successfully!'})
        except Exception as e:
            print(e)
            return make_response('Could not add order', 400, {'message': 'Please check your items!"'})


class OrderItem(Resource):

    @classmethod
    # @token_required
    def get(cls, restaurant_id, order_id):
        try:
            order = db.session.query(Order).filter_by(id=order_id).filter_by(restaurant_id=restaurant_id).first()
            return order.serialize()
        except:
            return make_response('Could not find order item', 400, {'message': 'Please check your order!"'})

    @classmethod
    # @token_required
    def put(cls, restaurant_id, order_id):

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Order.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            db_role = db.session.query(Order).filter_by(id=order_id).filter_by(restaurant_id=restaurant_id).first()
            data = request.get_json()
            db_role.user_id = data['user_id']
            db_role.restaurant_id = data['restaurant_id']
            db_role.menu_id = data['menu_id']
            db_role.qty = data['qty']
            db_role.status = data['status']

            db.session.commit()
        except:
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the Order"
            )

        return make_response('Success', 201, {'message': 'Successfully updated!"'})

    @classmethod
    # @token_required
    def delete(cls, restaurant_id, order_id):
        try:
            temp_data = db.session.query(Order).filter_by(id=order_id).filter_by(restaurant_id=restaurant_id).first()
            if temp_data is None:
                return make_response('Order not found!', 400, {'message': 'Order cannot be deleted!'})
        except:
            return create_error_message(
                500, "Internal server Error",
                "Error while retrieving information from db"
            )
        db.session.query(Order).filter_by(id=order_id).delete()
        db.session.commit()
        return make_response('Order successfully deleted', 201, {'message': 'Successfully deleted!'})

