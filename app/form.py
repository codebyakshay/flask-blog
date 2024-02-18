from flask_wtf import FlaskForm 
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    
    username = StringField('Username', 
                           validators=[DataRequired(), 
                                       Length(min=2,max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), 
                                    Email()])
    user_password = PasswordField('Password', 
                                  validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', 
                                     validators=[DataRequired(), 
                                                 EqualTo('user_password')])
    submit = SubmitField('Sign Up')
    
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That Username is taken Choose diffrent one")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That Email is taken Choose diffrent one")
        
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    user_password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login!')
    
    
class UpdateAccountForm(FlaskForm):
    
    username = StringField('Username', 
                           validators=[DataRequired(), 
                                       Length(min=2,max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), 
                                    Email()])
    
    submit = SubmitField('Update')
    
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That Username is taken Choose diffrent one")
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That Email is taken Choose diffrent one")