from flask import Blueprint, jsonify, request, render_template, url_for, flash, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_access_cookies
from flask_login import login_required, logout_user, current_user
from .utils import parse_data, camel_to_snake
from .models import User
from . import db
from werkzeug.security import check_password_hash

user = Blueprint('user', __name__)

@user.route('/all', methods=['GET'])
def all_users():
  users = User.query.all()
  parsed_users = [user.to_json() for user in users]
  return jsonify(users=parsed_users)
  
@user.route("/")
@login_required
def get_user():
  return render_template('user/profile.html', user=current_user)

@user.route('/', methods=['POST'])
# @jwt_required()
@login_required
def update_account():
  user = User.query.get(current_user.id)
  updated_data = parse_data(request)
  """
  for key, value in updated_data.items():
    if hasattr(user, camel_to_snake(key)):
      setattr(user, camel_to_snake(key), value)
  """
  user.first_name = updated_data.get('firstName')
  user.last_name = updated_data.get('lastName')
  user.email = updated_data.get('email')
  
  db.session.commit()
  # return jsonify(message="User data updated")
  flash("Updated successfully", category="success")
  return redirect(url_for("user.get_user"))

@user.route('/delete', methods=['POST'])
# @jwt_required()
@login_required
def delete_account():
  user = User.query.get(current_user.id)
  password = parse_data(request).get('password')
  
  print(user)
  
  if check_password_hash(user.password, password) is not True:
    flash("Incorrect password, account not deleted", category="error")
    return render_template("user/profile.html", user=current_user)
  
  db.session.delete(user)
  db.session.commit()
  
  # response = jsonify(message="Account deleted")
  # unset_access_cookies(response)
  # return response
  logout_user()
  flash("Account deleted", category="success")
  return redirect(url_for("auth.login"))