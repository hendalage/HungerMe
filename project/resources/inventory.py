from flask import Response, request, jsonify, make_response
from project.utils import create_error_message, token_required
from project.models.models import Menu, Restaurant, Inventory
from project import db
from jsonschema import validate, ValidationError
from flask_restful import Resource


class InventoryCollection(Resource):

    @classmethod
    # @token_required
    def get(cls, restaurant_id):
        inventory_collection = db.session.query(Inventory).filter_by(restaurant_id=restaurant_id).join(Restaurant).all()
        inventory_list = []
        print(inventory_collection)
        for item in inventory_collection:
            inventory_data = {
                'id': item.id,
                'restaurant_id': item.restaurant_id,
                'name': item.name,
                'description': item.description,
                'qty': item.qty,
                'restaurant_name': item.restaurant.name,
                'restaurant_address': item.restaurant.address,
                'restaurant_contact_no': item.restaurant.contact_no
            }
            inventory_list.append(inventory_data)
        return jsonify({'inventory_items': inventory_list})

    @classmethod
    # @token_required
    def post(cls, restaurant_id):
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
            new_item = Inventory(
                restaurant_id=restaurant_id,
                name=data['name'],
                description=data['description'],
                qty=data['qty']
            )

            db.session.add(new_item)
            db.session.commit()

            return jsonify({'message': 'New item added to the inventory successfully!'})
        except Exception as e:
            print(e)
            return make_response('Could not add inventory item', 400, {'message': 'Please check your entries!"'})


class InventoryItem(Resource):

    @classmethod
    # @token_required
    def get(cls, restaurant_id, inventory_id):
        try:
            inventory_item = db.session.query(Inventory).filter_by(id=inventory_id).filter_by(restaurant_id=restaurant_id).join(Restaurant).first()
            return inventory_item.serialize()
        except:
            return make_response('Could not find menu item', 400, {'message': 'Please check your entries!"'})

    @classmethod
    # @token_required
    def put(cls, restaurant_id, inventory_id):

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
            inventory_item = db.session.query(Inventory).filter_by(id=inventory_id).filter_by(restaurant_id=restaurant_id).first()
            data = request.get_json()

            inventory_item.name = data['name']
            inventory_item.description = data['description']
            inventory_item.qty = data['qty']
            db.session.commit()
        except:
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the inventory"
            )

        return make_response('Success', 201, {'message': 'Successfully updated!"'})

    @classmethod
    # @token_required
    def delete(cls, restaurant_id, inventory_id):
        try:
            temp_data = db.session.query(Inventory).filter_by(id=inventory_id).filter_by(restaurant_id=restaurant_id).first()
            if temp_data is None:
                return make_response('Item not found!', 400, {'message': 'Item cannot be deleted!'})
        except:
            return create_error_message(
                500, "Internal server Error",
                "Error while retrieving information from db"
            )
        db.session.query(Inventory).filter_by(id=inventory_id).filter_by(restaurant_id=restaurant_id).delete()
        db.session.commit()

        return make_response('Success', 204, {'message': 'Successfully deleted!"'})
