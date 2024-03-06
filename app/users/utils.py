import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from app import mail
from flask import current_app
from flask_login import current_user


def save_picture(form_picture):
    #change the file name to be unique
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_user.root_path, 'static/profile-pictures', picture_fn)
    
    #compress the image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)    

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender='noreply@codebyakshay.com',
                  recipients=[user.email])
    # Set email priority (1 = high, 3 = normal, 5 = low)
    msg.extra_headers = {'X-Priority': '1'}
    
    msg.body =  f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request, simply ignore this email and no changes will be made.'''
    mail.send(msg)
