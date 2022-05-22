from flask import Response, request, jsonify, make_response
from project.utils import *
from project.models.models import Menu, Restaurant, Inventory
from project import db
from jsonschema import validate, ValidationError
from flask_restful import Resource
from project.constants import *


class RestaurantCollection(Resource):

    @classmethod
    # @token_required
    def get(cls):
        body = HungerMeBuilder()

        body.add_namespace("hungerme", LINK_RELATIONS_URL)
        # body.add_control_restaurants_all()
        body.add_control("self", url_for("api.restaurantcollection"))
        body.add_control_add_restaurant()

        body["items"] = []

        restaurant_collection = db.session.query(Restaurant).all()
        for db_restaurant in restaurant_collection:
            item = HungerMeBuilder(
                db_restaurant.serialize()
            )
            # restaurant_data = item.serialize()
            item.add_control("self", url_for("api.restaurantitem", restaurant=db_restaurant))
            item.add_control_delete_restaurant(restaurant=db_restaurant)
            item.add_control_edit_restaurant(restaurant=db_restaurant)
            item.add_control("profile", RESTAURANT_PROFILE)

            body["items"].append(item)
        # return jsonify({'restaurant_items': restaurant_list})
        return Response(json.dumps(body), 200, mimetype=MASON)

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
        body = HungerMeBuilder(restaurant.serialize())
        body.add_namespace("hungerme", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.restaurantitem", restaurant=restaurant))
        body.add_control("profile", RESTAURANT_PROFILE)
        body.add_control("collection", url_for("api.restaurantcollection"))
        body.add_control_delete_restaurant(restaurant=restaurant)
        body.add_control_edit_restaurant(restaurant=restaurant)

        body.add_control_add_inventory(restaurant=restaurant)
        body.add_control_add_reservation(restaurant=restaurant)
        body.add_control_add_menu(restaurant=restaurant)
        body.add_control_add_order(restaurant=restaurant)

        return Response(json.dumps(body), 200, mimetype=MASON)

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
