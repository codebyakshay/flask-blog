import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, bcrypt, db
from app.form import RegistrationForm,LoginForm, UpdateAccountForm, PostForm
from app.models import User, Posts
from flask_login import login_user, current_user, logout_user, login_required
app.static_folder = 'static'




@app.route("/home")
@app.route("/")
def home():
    posts = Posts.query.all()
    return render_template('home.html', posts=posts) # type: ignore

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    reg_form_instance = RegistrationForm()
    if reg_form_instance.validate_on_submit():
        
        hashed_pwd = bcrypt.generate_password_hash(reg_form_instance.user_password.data).decode('utf-8')
        username = reg_form_instance.username.data
        email = reg_form_instance.email.data
        user = User(username = username, email = email, password = hashed_pwd) # type: ignore
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login','success')
        return redirect(url_for('login'))    
    return render_template('register.html',title='Register',reg_form=reg_form_instance)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    login_form_instance = LoginForm()
    if login_form_instance.validate_on_submit():
        
        user = User.query.filter_by(email=login_form_instance.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, 
                                               login_form_instance.user_password.data):
            
            login_user(user, remember=login_form_instance.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsucessful!, Please Check Email and Password','danger')

    return render_template('login.html',title='Login',login_form=login_form_instance)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))




def save_picture(form_picture):
    #change the file name to be unique
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile-pictures', picture_fn)
    
    #compress the image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)    

    return picture_fn



@app.route("/account", methods=['GET','POST'])
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
            return redirect(url_for('account'))
        
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
            
        image_file = url_for('static',filename=f"profile-pictures/{current_user.image_file}")
        
        return render_template('account.html', 
                            title='Account', image_file=image_file, form=form)
        
    except Exception as e:
        db.session.rollback()  # Rollback changes in case of an exception
        flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('account'))
    
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            post = Posts(title=form.title.data, content=form.content.data, user_id=current_user.id) # type: ignore
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating post: {e}', 'danger')
            # Optionally, log the error here
    return render_template('create_post.html', title='New Post', form=form)