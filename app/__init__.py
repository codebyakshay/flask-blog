import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from json import load
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['codebyakshay-vps'] = 'codebyakshay.com'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') 

# Set the static folder after initializing the app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') 
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # type: ignore
login_manager.login_message_category = 'info'

# Mail configuration
app.config['MAIL_SERVER'] = 'mail.codebyakshay.com'
app.config['MAIL_PORT'] = 465  # Typically 465 for SSL or 587 for TLS
app.config['MAIL_USE_TLS'] = False  # Set to True if your mail server uses TLS
app.config['MAIL_USE_SSL'] = True  # Set to True if your mail server uses SSL
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') 
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)

from app import routes
