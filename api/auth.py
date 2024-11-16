from flask import Blueprint, request, jsonify
from .utils import parse_data
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, set_refresh_cookies, jwt_required, unset_jwt_cookies

auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=['POST'])
def login():
  data = parse_data(request)
  email = data.get('email')
  password = data.get('password')
  
  if email is None or password is None:
    return jsonify({'message':'email and password are required'}), 400
  found_user = User.query.filter_by(email=email).first()
  print(found_user)
  if found_user is None or check_password_hash(found_user.password, password) is not True:
    return jsonify({'message':'Invalid login details'}), 400
  
  access_token=create_access_token(identity=found_user.id)
  refresh_token=create_refresh_token(identity=found_user.id)
  response = jsonify(access_token=access_token)
  set_refresh_cookies(response, refresh_token)
  return response

@auth.route('/signup', methods=["POST"])
def register():
  data = parse_data(request)
  first_name = data.get('firstName')
  last_name = data.get('lastName')
  email = data.get('email')
  password = data.get('password')
  
  if first_name is None or last_name is None or email is None or password is None:
    return jsonify({'mesasage':'firstname, lastname, email & password are required'}), 400
  # chack that user does not exist yet 
  # print(User.query.filter_by(email=email))
  if User.query.filter_by(email=email).first() is not None:
    return jsonify({'message':'Email already exists, please signin'})
  new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password, method='scrypt')) # pbkdf2:sha256 (default) or bcrypt (not working for some reason)
  db.session.add(new_user)
  db.session.commit()
  return jsonify({ 'message':'User registered' }), 201

@auth.route('/signout', methods=['POST'])
@jwt_required()
def logout():
  response = jsonify({'message':'User logged out'})
  unset_jwt_cookies(response)
  return response

@auth.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
  current_user_identity = get_jwt_identity()
  new_access_token = create_access_token(identity=current_user_identity)
  return jsonify(access_token=new_access_token)