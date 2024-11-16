from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_access_cookies
from .utils import parse_data, camel_to_snake
from .models import User
from . import db

user = Blueprint('user', __name__)

@user.route('/', methods=['GET'])
def all_users():
  users = User.query.all()
  parsed_users = [user.to_json() for user in users]
  return jsonify(users=parsed_users)

@user.route('/', methods=['PATCH'])
@jwt_required()
def update_account():
  user = User.query.get(int(get_jwt_identity()))
  updated_data = parse_data(request)
  for key, value in updated_data.items():
    if hasattr(user, camel_to_snake(key)):
      setattr(user, camel_to_snake(key), value)
    
  db.session.commit()
  return jsonify(message="User data updated")

@user.route('/', methods=['DELETE'])
@jwt_required()
def delete_account():
  user = User.query.get(int(get_jwt_identity()))
  
  db.session.delete(user)
  db.session.commit()
  
  response = jsonify(message="Account deleted")
  unset_access_cookies(response)
  return response