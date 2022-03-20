from copy import copy
from datetime import datetime, timedelta

import jwt
from flask_sqlalchemy import SQLAlchemy
from jsonschema import validate, ValidationError
from flask import Response, request, jsonify, make_response
from flask_restful import Resource
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from project.models.models import User
from project import db


class UserCollection(Resource):

    @classmethod
    def get(cls):
        return "true"

    @classmethod
    def post(cls):
        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = User(name=data['name'], email=data['email'], password=hashed_password, type=data['type'],
                        status=data['status'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'New user created!'})


class LoginCollection(Resource):

    @classmethod
    def post(cls):
        auth = request.get_json()

        if not auth or not auth['username'] or not auth['password']:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        user = db.session.query(User).filter_by(email=auth['username']).first()

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        if check_password_hash(user.password, auth['password']):
            token = jwt.encode(
                {'id': str(user.id), 'exp': datetime.utcnow() + timedelta(minutes=30)},
                'thisissecret')

            return jsonify({'token': token})

        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
