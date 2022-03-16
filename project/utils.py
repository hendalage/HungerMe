from functools import wraps

import jwt
from flask import abort, request, jsonify
from project.models.models import User


def create_error_message(status_code, error, message=None):
    """
    Method to create error message
    Return
        - Error object
    """
    error_message = {
        'Code': status_code,
        'Error': error,
        'Message': message
    }
    return abort(status_code, error_message)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, 'thisissecret')
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# def require_admin(func):
#     """
#     Method to validate admin key
#     """
#
#     def wrapper(*args, **kwargs):
#         api_key = request.headers.get("HRSystem-Api-Key")
#         if api_key is None:
#             return create_error_message(403, "Authentication Error")
#         key_hash = ApiKey.key_hash(
#             request.headers.get("HRSystem-Api-Key").strip())
#         db_key = ApiKey.query.filter_by(admin=True).first()
#         if secrets.compare_digest(key_hash, db_key.key):
#             return func(*args, **kwargs)
#         return create_error_message(403, "Authentication Error")
#     return wrapper


# def require_employee_key(func):
#     """
#     Method to validate employee key
#     """
#
#     def wrapper(self, employee, *args, **kwargs):
#         api_key = request.headers.get("HRSystem-Api-Key")
#         if api_key is None:
#             return create_error_message(403, "Authentication Error")
#         key_hash = ApiKey.key_hash(
#             request.headers.get("HRSystem-Api-Key").strip())
#         admin_db_key = ApiKey.query.filter_by(admin=True).first()
#         if secrets.compare_digest(key_hash, admin_db_key.key):
#             return func(self, employee, *args, **kwargs)
#         else:
#             db_key = ApiKey.query.filter_by(employee=employee).first()
#             if db_key is not None and secrets.compare_digest(
#                     key_hash, db_key.key):
#                 return func(self, employee, *args, **kwargs)
#             return create_error_message(403, "Authentication Error")
#
#     return wrapper
