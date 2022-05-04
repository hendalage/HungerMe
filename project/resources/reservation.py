from flask import Response, request, jsonify, make_response
from project.utils import create_error_message, token_required
from project.models.models import Menu, Restaurant, Inventory, Reservation
from project import db
from jsonschema import validate, ValidationError
from flask_restful import Resource
import datetime


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
                'date': reservation.date.strftime("%d/%m/%Y"),
                'from_time': reservation.from_time.strftime("%H:%M:%S"),
                'to_time': reservation.to_time.strftime("%H:%M:%S"),
                'created_at': reservation.created_at,
                'updated_at': reservation.updated_at,
                'description': reservation.description,
                'restaurant_name': reservation.restaurant.name,
                'restaurant_address': reservation.restaurant.address,
                'restaurant_contact_no': reservation.restaurant.contact_no
            }
            reservation_list.append(reservation_data)
        return jsonify({'current_reservations': reservation_list})

    @classmethod
    # @token_required
    def post(cls, restaurant_id):
        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Reservation.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            data = request.get_json()
            temp_data = db.session.query(Reservation).filter_by(user_id=data['user_id']).first()
            if temp_data is not None:
                return make_response(
                    'Only one reservation per user is allowed!', 400,
                    {'message': 'Could not add reservation'}
                )
        except Exception as e:
            print(e)
            return make_response(
                'Could not add reservation', 400,
                {'message': 'Please check your entries!'}
            )
        try:
            new_reservation = Reservation(
                user_id=data['user_id'],
                restaurant_id=restaurant_id,
                date=data['date'],
                from_time=data['from_time'],
                to_time=data['to_time'],
                description=data['description']
            )
            db.session.add(new_reservation)
            db.session.commit()
            return jsonify({'message': 'New item added to the reservation successfully!'})
        except Exception as e:
            print(e)
            return make_response('Could not add reservation', 400, {'message': 'Please check your entries!"'})


class ReservationItem(Resource):

    @classmethod
    # @token_required
    def get(cls, restaurant_id, user_id):  # 08bb1373-7b11-4d32-a5f4-d40cbf63fa3f
        try:
            reservation = db.session.query(Reservation).filter_by(user_id=user_id).filter_by(restaurant_id=restaurant_id).first()
            return reservation.serialize()
        except:
            return make_response('Could not find reservation', 400, {'message': 'Please check your entries!"'})

    @classmethod
    # @token_required
    def put(cls, restaurant_id, user_id):

        if not request.json:
            return create_error_message(
                415, "Unsupported media type",
                "Payload format is in an unsupported format"
            )

        try:
            validate(request.json, Reservation.get_schema())
        except ValidationError:
            return create_error_message(
                400, "Invalid JSON document",
                "JSON format is not valid"
            )

        try:
            reservation = db.session.query(Reservation).filter_by(user_id=user_id).filter_by(restaurant_id=restaurant_id).first()
            data = request.get_json()

            reservation.date = datetime.datetime.strptime(data['date'], "%d-%m-%Y").date()
            reservation.from_time = datetime.datetime.strptime(data['from_time'], "%H:%M:%S").time()
            reservation.to_time = datetime.datetime.strptime(data['to_time'], "%H:%M:%S").time()
            reservation.description = data['description']
            db.session.commit()
        except:
            return create_error_message(
                500, "Internal server Error",
                "Error while updating the reservation"
            )

        return make_response('Success', 201, {'message': 'Successfully updated!"'})

    @classmethod
    #@token_required
    def delete(cls, restaurant_id, user_id):
        try:
            temp_data = db.session.query(Reservation).filter_by(user_id=user_id).filter_by(restaurant_id=restaurant_id).first()
            if temp_data is None:
                return make_response('Reservation not found!', 400, {'message': 'Reservation cannot be deleted!'})
        except:
            return create_error_message(
                500, "Internal server Error",
                "Error while retrieving information from db"
            )
        db.session.query(Reservation).filter_by(user_id=user_id).delete()
        db.session.commit()
        return make_response('Reservation successfully deleted', 201, {'message': 'Successfully deleted!'})
