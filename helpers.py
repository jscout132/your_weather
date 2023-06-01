from functools import wraps
# import secrets
from flask import request, jsonify, json
from json import JSONEncoder
import decimal

from models import User
# remember to import favoritecity

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        id = None

        if 'x-access-token' in request.headers:
            id=request.headers['x-access-token'].split(' ')[1]
        if not id:
            return jsonify({'message': 'token is missing'}), 401
        
        try:
            current_user_token = User.query.filter_by(id=id).first()
        except:
            owner = User.query.filter_by(id = id).first()

            if id!=owner.id:
                return jsonify({'message':'id is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

class Encoding(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(Encoding, self).default(obj)