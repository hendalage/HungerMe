from flask import Response, request, jsonify, make_response
from project.utils import create_error_message, token_required
from project.models.models import Menu, Restaurant
from project import db
from jsonschema import validate, ValidationError
from flask_restful import Resource


class MenuCollection(Resource):

    @classmethod
    # @token_required
    def get(cls, restaurant):
        menus = db.session.query(Menu).filter_by(restaurant_id=restaurant.id).join(Restaurant).all()
        menu_list = []
        # print(menus)
        for menu in menus:
            menu_data = menu.serialize()
            # menu_data = {
            #     'id': menu.id,
            #     'name': menu.name,
            #     'description': menu.description,
            #     'restaurant_id': menu.restaurant_id,
            #     'price': menu.price,
            #     'status': menu.status,
            #     'restaurant_name': menu.restaurant.name,
            #     'restaurant_address': menu.restaurant.address,
            #     'restaurant_contact_no': menu.restaurant.contact_no
            # }
            menu_list.append(menu_data)

        return jsonify({'menus': menu_list})

    @classmethod
    # @token_required
    def post(cls, restaurant):
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )
        try:
            validate(request.json, Menu.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )
        try:
            data = request.get_json()
            new_menu = Menu(
                name=data['name'],
                description=data['description'],
                restaurant_id=restaurant.id,
                price=data['price'],
                status=data['status']
            )
            db.session.add(new_menu)
            db.session.commit()
            return jsonify({'message': 'New menu added successfully!'})
        except Exception as e:
            print(e)
            return make_response('Could not add menu item', 400, {'message': 'Please check your entries!"'})


class MenuItem(Resource):

    @classmethod
    # @token_required
    def get(cls, restaurant, menu_id):
        menu = db.session.query(Menu).filter_by(id=menu_id).first()
        if menu is not None:
            return menu.serialize()
        else:
            return make_response('Could not find menu item', 400, {'message': 'Please check your entries!"'})

    @classmethod
    # @token_required
    def put(cls, restaurant, menu_id):
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )
        try:
            validate(request.json, Menu.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )
        try:
            menu_item = db.session.query(Menu).filter_by(id=menu_id).first()
            data = request.get_json()
            menu_item.name = data['name']
            menu_item.description = data['description']
            menu_item.price = data['price']
            db.session.commit()
        except:
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the menu"
            )
        return make_response('Success', 201, {'message': 'Successfully updated!"'})

    @classmethod
    # @token_required
    def delete(cls, restaurant, menu_id):
        try:
            temp_data = db.session.query(Menu).filter_by(id=menu_id).first()
            if temp_data is None:
                return make_response('Menu not found!', 400, {'message': 'Menu cannot be deleted!'})
        except:
            return create_error_message(
                500, "Internal server Error",
                "Error while retrieving information from db"
            )
        db.session.query(Menu).filter_by(id=menu_id).delete()
        db.session.commit()
        return make_response('Menu successfully deleted', 201, {'message': 'Successfully deleted!"'})
