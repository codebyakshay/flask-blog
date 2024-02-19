from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from json import load
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['codebyakshay-vps'] = 'codebyakshay.com'
app.config['SECRET_KEY'] = 'a088ebee2a35433284d75ded248f5fb7a82da16af3bae050dcd14d0329885414'

# Set the static folder after initializing the app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from app import routes
