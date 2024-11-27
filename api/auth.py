from flask import Blueprint, request, jsonify, render_template, flash, url_for, redirect
from .utils import parse_data, check_empty_field
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, set_refresh_cookies, jwt_required, unset_jwt_cookies
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=["GET", 'POST'])
def login():
  if request.method == "GET":
    return render_template("auth/login.html")
    
  data = parse_data(request)
  email = data.get('email')
  password = data.get('password')
  
  if check_empty_field(email=email, password=password) == False:
    # return jsonify({'message':'email and password are required'}), 400
    flash("Email and password required", category="error")
    return render_template("auth/login.html", email=email, password=password)
  found_user = User.query.filter_by(email=email).first()
  
  if found_user is None:
    # return jsonify({'message':'Invalid login details'}), 400
    flash("Invalid login", category="error")
    return render_template("auth/login.html", email=email, password=password)
    
  if check_password_hash(found_user.password, password) is not True:
    # return jsonify({'message':'Invalid login details'}), 400
    flash("Invalid login", category="error")
    return render_template("auth/login.html", email=email, password=password)
  
  """
  access_token=create_access_token(identity=found_user.id)
  refresh_token=create_refresh_token(identity=found_user.id)
  response = jsonify(access_token=access_token)
  set_refresh_cookies(response, refresh_token)
  return response
  """
  login_user(found_user)
  flash("User logged in", category="success")
  return redirect("/")


@auth.route('/signup', methods=["GET", "POST"])
def register():
  if request.method == "GET":
    return render_template("auth/register.html")
    
  data = parse_data(request)
  first_name = data.get('firstName')
  last_name = data.get('lastName')
  email = data.get('email')
  password1 = data.get('password1')
  password2 = data.get('password2')
  
  if check_empty_field(first_name=first_name, last_name=last_name, email=email, password=password1) == False:
    # return jsonify({'mesasage':'firstname, lastname, email & password are required'}), 400
    flash("All fields required", category="error")
    return render_template("auth/register.html", firstname=first_name, lastname=last_name, email=email, password1=password1, password2=password2)
  
  if password2 != password1:
    flash("Passwords don't match", category="error")
    return render_template("auth/register.html", firstname=first_name, lastname=last_name, email=email, password1=password1, password2=password2)
    
  # chack that user does not exist yet 
  # print(User.query.filter_by(email=email))
  if User.query.filter_by(email=email).first() is not None:
    # return jsonify({'message':'Email already exists, please signin'})
    flash("Email already exists, please sign in", category="error")
    return render_template("auth/register.html", firstname=first_name, lastname=last_name, email=email, password1=password1, password2=password2)
    
  new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password1, method='scrypt')) # pbkdf2:sha256 (default) or bcrypt (not working for some reason)
  db.session.add(new_user)
  db.session.commit()
  # return jsonify({ 'message':'User registered' }), 201
  flash("User registered", category="success")
  return redirect(url_for("auth.login"))

@auth.route('/signout', methods=['POST'])
@login_required
def logout():
  """
  response = jsonify({'message':'User logged out'})
  unset_jwt_cookies(response)
  return response
  """
  logout_user()
  return redirect("/")

"""
@auth.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
  current_user_identity = get_jwt_identity()
  new_access_token = create_access_token(identity=current_user_identity)
  return jsonify(access_token=new_access_token)
"""