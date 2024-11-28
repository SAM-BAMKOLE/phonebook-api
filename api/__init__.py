from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

APP_VERSION= os.getenv('APP_VERSION') # 1.0
BASE_ROUTE= os.getenv('BASE_ROUTE') # 'api'
DB_NAME = os.getenv('DATABASE_URI') # 'database.db'

db = SQLAlchemy()
jwt = JWTManager()
login_manager = LoginManager()

def init_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
  app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME if os.getenv('FLASK_ENV') == 'production' else "sqlite:///database.db"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
  """
  app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
  app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)
  app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
  app.config['JWT_COOKIE_SECURE'] = False
  app.config['JWT_COOKIE_CSRF_PROTECT'] = True
  """
  
  db.init_app(app)
  jwt.init_app(app)
  
  from .auth import auth
  from .contact import contact
  from .user import user
  
  app.register_blueprint(auth, url_prefix=f'/auth')
  app.register_blueprint(contact, url_prefix='/')
  app.register_blueprint(user, url_prefix='/user')

  login_manager.init_app(app)
  login_manager.login_view = "auth.login"

  @login_manager.user_loader
  def load_user(id):
      return User.query.get(id)
  
  from .models import User
  
  with app.app_context():
    create_db()
  
  return app
  
def create_db():
  if os.getenv("FLASK_ENV") !=  "production" and not os.path.exists('api/'+DB_NAME):
    db.create_all()
    print('Database created')
