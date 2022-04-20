from flask import Response, request, jsonify, make_response
from project.utils import create_error_message, token_required
from project.models.models import Restaurant, User, Oder
from project import db
from jsonschema import validate, ValidationError
from flask_restful import Resource


class OderCollection(Resource):

    @classmethod
    # @token_required
    def get(cls, restaurant_id):
        oders = db.session.query(Oder).filter_by(restaurant_id=restaurant_id).join(Restaurant).join(User).all()

        oder_list = []
        print(oders)
        for oder in oders:
            oder_data = {}
            oder_data['id'] = oder.id
            oder_data['name'] = oder.name
            oder_data['description'] = oder.description
            oder_data['restaurant_id'] = oder.restaurant_id
            oder_data['price'] = oder.price
            oder_data['status'] = oder.status
            oder_data['restaurant_name'] = oder.restaurant.name
            oder_data['restaurant_address'] = oder.restaurant.address
            oder_data['restaurant_contact_no'] = oder.restaurant.contact_no
            oder_data['user_name'] = oder.user.name
            oder_data['user_contact_no'] = oder.user.contact_no
            oder_data['user_address'] = oder.user.address
            oder_list.append(oder_data)

        return jsonify({'oders': oder_list})


class OderItem(Resource):

    @classmethod
    # @token_required
    def get(cls, oder_id):

        try:
            oder = db.session.query(Oder).filter_by(id=oder_id).join(Restaurant).first()

            return oder.serialize()
        except:
            return make_response('Could not find oder item', 400, {'message': 'Please check your oder!"'})

    @classmethod
    # @token_required
    def post(cls):

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Oder.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            data = request.get_json()

            new_oder = Oder(name=data['name'], description=data['description'], restaurant_id=data['restaurant_id'], price=data['price'],
                            status=data['status'])

            db.session.add(new_oder)
            db.session.commit()

            return jsonify({'message': 'New oder added successfully!'})
        except Exception as e:
            print(e)
            return make_response('Could not add oder', 400, {'message': 'Please check your items!"'})

    @classmethod
    # @token_required
    def put(cls, oder_id):

        db_role = Oder.query.filter_by(id=oder_id).first()

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Oder.get_schema())
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
    def delete(cls, oder_id):
        db.session.query().filter_by(id=oder_id).delete()
        db.session.commit()

        return make_response('Success', 204, {'message': 'Successfully deleted!"'})
