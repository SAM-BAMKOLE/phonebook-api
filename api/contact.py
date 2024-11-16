from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import parse_data, camel_to_snake
from .models import Contact
from . import db

contact = Blueprint('contact', __name__)

@contact.route('/', methods=["GET"])
@jwt_required()
def get_user_contacts():
  contacts = Contact.query.filter(Contact.holder_id==get_jwt_identity())
  parsed_contacts = [item.to_json() for item in contacts]
  
  return jsonify(contacts=parsed_contacts)
  
@contact.route('/', methods=['POST'])
@jwt_required()
def add_contact():
  data = parse_data(request)
  first_name = data.get('firstName')
  last_name = data.get('lastName')
  email = data.get('email')
  phone_number = data.get('phoneNumber')
  
  new_contact = Contact(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, holder_id=get_jwt_identity())
  
  db.session.add(new_contact)
  db.session.commit()
  
  return jsonify(message="New contact added", contact_id=new_contact.id), 201

@contact.route('/<int:contact_id>')
@jwt_required()
def get_contact(contact_id):
  contact = Contact.query.filter_by(id=contact_id).first()
  
  if not contact:
    return jsonify(message="You don't have this contact"), 404
  if contact.holder_id != get_jwt_identity():
    return jsonify(message="You do not have this contact"), 401
  
  return jsonify(contact=contact.to_json())

@contact.route('/<int:contact_id>', methods=['PATCH'])
@jwt_required()
def update_contact(contact_id):
  updated_data = parse_data(request)
  contact = Contact.query.filter_by(id=contact_id).first()
  if not contact:
    return jsonify(message="You don't have this contact"), 404
  if contact.holder_id != get_jwt_identity():
    return jsonify(message="You do not have this contact"), 401
    
  for key, value in updated_data.items():
    if hasattr(contact, camel_to_snake(key)):
      setattr(contact, camel_to_snake(key), value)
      
  db.session.commit()
  return jsonify(message='Contact updated', contact_id=contact.id)
  
@contact.route('/<int:contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
  contact= Contact.query.get(contact_id)
  if not contact:
    return jsonify(message="You don't have this contact"), 404
  if contact.holder_id != get_jwt_identity():
    return jsonify(message="You do not have this contact"), 401
    
  db.session.delete(contact)
  db.session.commit()
  return jsonify(message='Contact deleted')