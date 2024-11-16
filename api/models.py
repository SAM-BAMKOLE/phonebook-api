from . import db
from datetime import datetime

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(100), nullable=False)
  last_name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(150), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  contacts = db.relationship('Contact', backref='holder', lazy=True, cascade="all,delete-orphan")
  
  def to_json(self):
    return {
      "id": self.id,
      'firstName': self.first_name,
      'lastName': self.last_name,
      'email': self.email,
      # 'password': self.password,
      # 'created_at': self.created_at,
      # 'updated_at': self.updated_at
    }

class Contact(db.Model):
  __tablename__ = 'contacts'
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(100))
  last_name = db.Column(db.String(100))
  email = db.Column(db.String(150))
  phone_number = db.Column(db.String(17))
  holder_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  
  def to_json(self):
    return {
      'id': self.id,
      'firstName': self.first_name,
      'lastName': self.last_name,
      'email': self.email,
      'phoneNumber': self.phone_number,
    }
  