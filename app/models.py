from app import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import  SignatureExpired, BadSignature


from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
import time


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(20), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    image_file: str = db.Column(db.String(120), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Posts', 
                            backref='author', lazy=True)    
        
    
    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        token = s.dumps({'user_id': self.id})
        return token
    
    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            # Attempt to load the token with the specified maximum age
            data = s.loads(token, max_age=max_age)
            user_id = data['user_id']
            return User.query.get(user_id)
        except SignatureExpired:
            print("The token has expired.")
            return None
        except BadSignature:
            print("Invalid token.")
            return None
    
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    
    
    
    
    
    
    
    
    #def get_reset_token(self, expires_sec=1800):
    #    s = Serializer(app.config['SECRET_KEY'], expires_sec) # type: ignore
    #    return s.dumps({'user_id': int(self.id)})
    
    #@staticmethod
    #def verify_reset_token(token):
    #    s = Serializer(app.config['SECRET_KEY'])
    #    try:
    #        user_id = s.loads(token)
    #    except (SignatureExpired, BadSignature):
    #        return None
    #    return User.query.get(user_id)
    
    
   

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    
    def __repr__(self):
        return f"Posts('{self.title}', '{self.date_posted}')"

