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
            restaurant_data = item.serialize()
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
    def get(cls, restaurant):
        return restaurant.serialize()

    @classmethod
    # @token_required
    def put(cls, restaurant):

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
    def delete(cls, restaurant):
        db.session.query(Restaurant).filter_by(name=restaurant.name).delete()
        db.session.commit()

        return make_response('Restaurant deleted successfully', 201, {'message': 'Successfully deleted!"'})
