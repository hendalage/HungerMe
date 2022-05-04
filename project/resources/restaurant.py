from flask import Response, request, jsonify, make_response
from project.utils import create_error_message, token_required
from project.models.models import Menu, Restaurant, Inventory
from project import db
from jsonschema import validate, ValidationError
from flask_restful import Resource


class RestaurantCollection(Resource):

    @classmethod
    # @token_required
    def get(cls):
        restaurant_collection = db.session.query(Restaurant).all()
        restaurant_list = []
        for item in restaurant_collection:
            restaurant_data = {
                'id': item.id,
                'name': item.name,
                'address': item.address,
                'contact_no': item.contact_no,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
            }
            restaurant_list.append(restaurant_data)
        return jsonify({'restaurant_items': restaurant_list})

    @classmethod
    # @token_required
    def post(cls):
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Restaurant.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            data = request.get_json()

            new_restaurant = Restaurant(name=data['name'], address=data['address'], contact_no=data['contact_no'])

            db.session.add(new_restaurant)
            db.session.commit()

            return jsonify({'message': 'New restaurant added successfully!'})
        except Exception as e:
            print(e)
            return make_response('Could not add restaurant', 400, {'message': 'Please check your entries!"'})


class RestaurantItem(Resource):

    @classmethod
    # @token_required
    def get(cls, restaurant_id):
        try:
            restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).first()
            return restaurant.serialize()
        except:
            return make_response('Could not find restaurant', 400, {'message': 'Please check your entries!"'})

    @classmethod
    # @token_required
    def put(cls, restaurant_id):

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Restaurant.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )
        try:
            restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).first()
            data = request.get_json()

            restaurant.name = data['name']
            restaurant.address = data['address']
            restaurant.contact_no = data['contact_no']

            db.session.commit()
        except:
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the restaurant"
            )

        return make_response('Success', 201, {'message': 'Successfully updated!"'})

    @classmethod
    # @token_required
    def delete(cls, restaurant_id):
        try:
            temp_data = db.session.query(Restaurant).filter_by(id=restaurant_id).first()
            if temp_data is None:
                return make_response('Restaurant not found!', 400, {'message': 'Restaurant cannot be deleted!'})
        except:
            return create_error_message(
                500, "Internal server Error",
                "Error while retrieving information from db"
            )
        db.session.query(Restaurant).filter_by(id=restaurant_id).delete()
        db.session.commit()

        return make_response('Restaurant deleted successfully', 201, {'message': 'Successfully deleted!"'})
