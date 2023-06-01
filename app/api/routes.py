from flask import Blueprint, request, jsonify

from helpers import token_required
from models import sqla, FavoriteCities, city_schema, cities_schema, User

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/addcity', methods=['POST'])
@token_required
def addcity(current_user_token):
    id = request.json['id']
    city = request.json['city']
    user_id = current_user_token.id

    new_city = FavoriteCities(id = id,
                              city = city,
                              user_id=user_id)
    
    sqla.session.add(new_city)
    sqla.commit()
    response = city_schema.dump(new_city)
    return jsonify(response)