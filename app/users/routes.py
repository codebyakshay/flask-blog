from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Posts
from app.users.form import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from app.users.utils import save_picture, send_reset_email

users = Blueprint('users',__name__)


@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    reg_form_instance = RegistrationForm()
    if reg_form_instance.validate_on_submit():
        
        hashed_pwd = bcrypt.generate_password_hash(reg_form_instance.user_password.data).decode('utf-8')
        username = reg_form_instance.username.data
        email = reg_form_instance.email.data
        user = User(username = username, email = email, password = hashed_pwd) # type: ignore
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login','success')
        return redirect(url_for('users.login'))    
    return render_template('register.html',title='Register',reg_form=reg_form_instance)


@users.route("/login", methods=['GET','POST']) #login-Route
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    login_form_instance = LoginForm()
    if login_form_instance.validate_on_submit():
        
        user = User.query.filter_by(email=login_form_instance.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, 
                                               login_form_instance.user_password.data):
            
            login_user(user, remember=login_form_instance.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login unsucessful!, Please Check Email and Password','danger')

    return render_template('login.html',title='Login',login_form=login_form_instance)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    try:
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
                
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Account has been updated','success')
            return redirect(url_for('users.account'))
        
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
            
        image_file = url_for('static',filename=f"profile-pictures/{current_user.image_file}")
        
        return render_template('account.html', 
                            title='Account', image_file=image_file, form=form)
        
    except Exception as e:
        db.session.rollback()  # Rollback changes in case of an exception
        flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('main.account'))
    
@users.route("/user/<string:username>")  
def user_post(username):
    page = request.args.get('page', 1, type=int)  
    user = User.query.filter_by(username=username).first_or_404()
    posts = Posts.query.filter_by(author=user)\
        .order_by(Posts.date_posted.desc())\
        .paginate(page=page, per_page=5)  # Adjusted per_page to 5 as in the first function
    return render_template('user_post.html', posts=posts, user=user)  # Adjusted to use 'user_posts.html'

@users.route("/reset_password", methods=['GET', 'POST'])# type: ignore
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))    
    form = RequestResetForm()
    if form.validate_on_submit():   
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('A reset link has been sent to your email.','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', legend='Reset Password', 
                           title='Reset Password', form=form)  # Adjusted to use 'user_posts.html'

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))   
    user = User.verify_reset_token(token)
    
    if user is None:
        flash('That is an invalid token try sending in reset link again', 'warning')
        return redirect(url_for('users.reset_request'))
        
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.user_password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash(f'Your Password has been Updated ','success')
        return redirect(url_for('users.login'))    
    
    return render_template('reset_token.html', legend='Reset Password', 
                           title='Reset Password', form=form)