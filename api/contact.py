from flask import Blueprint, jsonify, request, flash, url_for, redirect, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import login_required, current_user
from .utils import parse_data, camel_to_snake
from .models import Contact
from . import db
from sqlalchemy import or_

contact = Blueprint('contact', __name__)

@contact.route("/", methods=["GET"])
@login_required
def home_page():
  contacts = Contact.query.filter(Contact.holder_id==current_user.id).all()
  return render_template("index.html", user=current_user, contacts=contacts)

@contact.route('/contacts', methods=["GET"])
# @jwt_required()
@login_required
def get_user_contacts():
  contacts = Contact.query.filter(Contact.holder_id==get_jwt_identity())
  # parsed_contacts = [item.to_json() for item in contacts]
  
  # return jsonify(contacts=parsed_contacts)
  return render_template("contact/index.html", contacts=contacts)
  
@contact.route('/contact/', methods=["GET", 'POST'])
# @jwt_required()
@login_required
def add_contact():
  contact = {
    "first_name": "",
    "last_name": "",
    "email":"",
    "phone_number":""
  }
  
  if request.method == "GET":
    return render_template("contact/new.html", contact=contact)
    
    
  data = parse_data(request)
  first_name = data.get('firstName')
  last_name = data.get('lastName')
  email = data.get('email') if data.get('email') is not None else ''
  phone_number = data.get('phoneNumber')
  
  new_contact = Contact(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, holder_id=current_user.id)
  
  if not first_name or not last_name or not phone_number:
    flash("firstname, lastName & phoneNumber are required", category="error")
    return render_template("contact/new.html", contact=new_contact)
  
  db.session.add(new_contact)
  db.session.commit()
  
  # return jsonify(message="New contact added", contact_id=new_contact.id), 201
  flash("Contact added", category="success")
  return redirect(url_for("contact.get_contact", contact_id=new_contact.id))

@contact.route('/contact/<int:contact_id>', methods=["GET"])
# @jwt_required()
@login_required
def get_contact(contact_id):
  contact = Contact.query.filter_by(id=contact_id).first()
  
  if not contact:
    # return jsonify(message="You don't have this contact"), 404
    flash("No contact with this id", category="error")
    return render_template("contact/contact.html")
    
  if contact.holder_id != current_user.id:
    # return jsonify(message="You do not have this contact"), 401
    flash("You dont have a contact with this id", category="error")
    return render_template("contact/contact.html")
  
  # return jsonify(contact=contact.to_json())
  return render_template("contact/contact.html", contact=contact)

@contact.route('/contact/<int:contact_id>', methods=['POST'])
# @jwt_required()
@login_required
def update_contact(contact_id):
  updated_data = parse_data(request)
  contact = Contact.query.filter_by(id=contact_id).first()
  if not contact:
    # return jsonify(message="You don't have this contact"), 404
    flash("You dont have a contact with this id", category="error")
    return render_template("contact/contact.html", contact=contact)
    
  if contact.holder_id != current_user.id:
    # return jsonify(message="You do not have this contact"), 401
    flash("This is not none of your contacts", category="error")
    return render_template("contact/contact.html", contact=contact)
   
  """ 
  for key, value in updated_data.items():
    if hasattr(contact, camel_to_snake(key)):
      setattr(contact, camel_to_snake(key), value)
  """
  
  contact.first_name = updated_data.get('firstname')
  contact.last_name = updated_data.get('lastname')
  contact.email = updated_data.get('email')
  contact.phone_number = updated_data.get('phoneNumber')
  
  print(contact.to_json())
  db.session.commit()
  # return jsonify(message='Contact updated', contact_id=contact.id)
  flash("Contact updated", category="success")
  return redirect(url_for("contact.get_contact", contact_id=contact.id))
  
@contact.route('/contact/<int:contact_id>', methods=['DELETE'])
# @jwt_required()
@login_required
def delete_contact(contact_id):
  contact= Contact.query.get(contact_id)
  if not contact:
    # return jsonify(message="You don't have this contact"), 404
    flash("You dont have a contact with this id", category="error")
    # return render_template("contact/contact.html")
    return jsonify(status="success"), 401
    
  if contact.holder_id != current_user.id:
    # return jsonify(message="You do not have this contact"), 401
    flash("This is not one of your contacts", category="error")
    # return render_template("contact/contact.html")
    return jsonify(status="error"), 401
    
  db.session.delete(contact)
  db.session.commit()
  # return jsonify(message='Contact deleted')
  flash("Contact deleted", category="success")
  # return redirect("contact/index.html")
  return jsonify(status="success"), 200

@contact.route("/contact/filter")
def filter_contact():
  query = request.args.get("search")
  
  filtered_contacts = Contact.query.filter(Contact.holder_id==current_user.id, or_(
    Contact.first_name.ilike(f"%{query}%"),
    Contact.last_name.ilike(f"%{query}%")
    )).all()
  
  contacts=[contact.to_json() for contact in filtered_contacts]
  
  return jsonify(contacts=contacts)