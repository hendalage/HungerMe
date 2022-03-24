from flask import Response, request, jsonify, make_response
from project.utils import create_error_message, token_required
from project.models.models import Menu, Restaurant
from project import db
from jsonschema import validate, ValidationError
from flask_restful import Resource


class MenuCollection(Resource):

    @classmethod
    @token_required
    def get(cls, restaurant_id):
        menus = db.session.query(Menu).filter_by(restaurant_id=restaurant_id).join(Restaurant).all()

        menu_list = []
        print(menus)
        for menu in menus:
            menu_data = {}
            menu_data['id'] = menu.id
            menu_data['name'] = menu.name
            menu_data['description'] = menu.description
            menu_data['restaurant_id'] = menu.restaurant_id
            menu_data['price'] = menu.price
            menu_data['status'] = menu.status
            menu_data['restaurant_name'] = menu.restaurant.name
            menu_data['restaurant_address'] = menu.restaurant.address
            menu_data['restaurant_contact_no'] = menu.restaurant.contact_no
            menu_list.append(menu_data)

        return jsonify({'menus': menu_list})


class MenuItem(Resource):

    @classmethod
    @token_required
    def get(cls, menu_id):

        try:
            menu = db.session.query(Menu).filter_by(id=menu_id).join(Restaurant).first()

            return menu.serialize()
        except:
            return make_response('Could not find menu item', 400, {'message': 'Please check your entries!"'})

    @classmethod
    @token_required
    def post(cls):

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

            new_menu = Menu(name=data['name'], description=data['description'], restaurant_id=data['restaurant_id'], price=data['price'],
                            status=data['status'])

            db.session.add(new_menu)
            db.session.commit()

            return jsonify({'message': 'New menu added successfully!'})
        except Exception as e:
            print(e)
            return make_response('Could not add menu item', 400, {'message': 'Please check your entries!"'})

    @classmethod
    @token_required
    def put(cls, menu_id):

        db_role = Menu.query.filter_by(id=menu_id).first()

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

        data = request.get_json()
        db_role.name = data['name']
        db_role.description = data['description']
        db_role.name = data['price']

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
    def delete(cls, menu_id):
        db.session.query().filter_by(id=menu_id).delete()
        db.session.commit()

        return make_response('Success', 204, {'message': 'Successfully deleted!"'})
