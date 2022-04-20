from flask import Response, request, jsonify, make_response
from project.utils import create_error_message, token_required
from project.models.models import Restaurant, User, Order
from project import db
from jsonschema import validate, ValidationError
from flask_restful import Resource


class OrderCollection(Resource):

    @classmethod
    # @token_required
    def get(cls, restaurant_id):
        orders = db.session.query(Order).filter_by(restaurant_id=restaurant_id).join(Restaurant).join(User).all()

        order_list = []
        print(orders)
        for order in orders:
            order_data = {}
            order_data['id'] = order.id
            order_data['name'] = order.name
            order_data['description'] = order.description
            order_data['restaurant_id'] = order.restaurant_id
            order_data['price'] = order.price
            order_data['status'] = order.status
            order_data['restaurant_name'] = order.restaurant.name
            order_data['restaurant_address'] = order.restaurant.address
            order_data['restaurant_contact_no'] = order.restaurant.contact_no
            order_data['user_name'] = order.user.name
            order_data['user_contact_no'] = order.user.contact_no
            order_data['user_address'] = order.user.address
            order_list.append(order_data)

        return jsonify({'orders': order_list})


class OrderItem(Resource):

    @classmethod
    # @token_required
    def get(cls, order_id):

        try:
            order = db.session.query(Order).filter_by(id=order_id).join(Restaurant).join(User). first()

            return order.serialize()
        except:
            return make_response('Could not find order item', 400, {'message': 'Please check your order!"'})

    @classmethod
    # @token_required
    def post(cls):

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

            new_order = Order(user_id=data['user_id'], restaurant_id=data['restaurant_id'], menu_id=data['menu_id'], qty=data['qty'], status=data['status'])

            db.session.add(new_order)
            db.session.commit()

            return jsonify({'message': 'New order added successfully!'})
        except Exception as e:
            print(e)
            return make_response('Could not add order', 400, {'message': 'Please check your items!"'})

    @classmethod
    # @token_required
    def put(cls, order_id):

        db_role = Order.query.filter_by(id=order_id).first()

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

        data = request.get_json()
        db_role.name = data['name']
        db_role.description = data['description']
        db_role.price = data['price']

        try:
            db.session.commit()
        except:
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the menu"
            )

        return make_response('Success', 201, {'message': 'Successfully updated!"'})

    @classmethod
    @token_required
    def delete(cls, order_id):
        db.session.query().filter_by(id=order_id).delete()
        db.session.commit()

        return make_response('Success', 204, {'message': 'Successfully deleted!"'})
