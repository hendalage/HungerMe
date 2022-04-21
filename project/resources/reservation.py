from flask import Response, request, jsonify, make_response
from project.utils import create_error_message, token_required
from project.models.models import Menu, Restaurant, Inventory, Reservation
from project import db
from jsonschema import validate, ValidationError
from flask_restful import Resource


class ReservationCollection(Resource):

    @classmethod
    # @token_required
    def get(cls, restaurant_id):
        reservation_collection = db.session.query(Reservation).filter_by(restaurant_id=restaurant_id).join(Restaurant).all()
        reservation_list = []
        print(reservation_collection)
        for reservation in reservation_collection:
            reservation_data = {
                'id': reservation.id,
                'user_id': reservation.user_id,
                'restaurant_id': reservation.restaurant_id,
                'date': reservation.date,
                'from_time': reservation.from_time,
                'to_time': reservation.to_time,
                'created_at': reservation.created_at,
                'updated_at': reservation.updated_at,
                'description': reservation.description,
                'restaurant_name': reservation.restaurant.name,
                'restaurant_address': reservation.restaurant.address,
                'restaurant_contact_no': reservation.restaurant.contact_no
            }
            reservation_list.append(reservation_data)
        return jsonify({'inventory_items': reservation_list})


class ReservationItem(Resource):

    @classmethod
    # @token_required
    def get(cls, user_id):  # 08bb1373-7b11-4d32-a5f4-d40cbf63fa3f
        try:
            reservation = db.session.query(Reservation).filter_by(id=user_id).join(Restaurant).first()
            return reservation.serialize()
        except:
            return make_response('Could not find reservation', 400, {'message': 'Please check your entries!"'})

    @classmethod
    # @token_required
    def post(cls):
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Inventory.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            data = request.get_json()

            new_item = Inventory(restaurant_id=data['restaurant_id'], name=data['name'], description=data['description'], qty=data['qty'])

            db.session.add(new_item)
            db.session.commit()

            return jsonify({'message': 'New item added to the inventory successfully!'})
        except Exception as e:
            print(e)
            return make_response('Could not add inventory item', 400, {'message': 'Please check your entries!"'})

    @classmethod
    # @token_required
    def put(cls, inventory_id):

        inventory_item = Inventory.query.filter_by(id=inventory_id).first()

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Inventory.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        data = request.get_json()
        inventory_item.name = data['name']
        inventory_item.description = data['description']
        inventory_item.price = data['price']

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
    def delete(cls, inventory_id):
        db.session.query().filter_by(id=inventory_id).delete()
        db.session.commit()

        return make_response('Success', 204, {'message': 'Successfully deleted!"'})
