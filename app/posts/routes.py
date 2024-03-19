from flask_login import login_user, current_user, logout_user, login_required
from flask import (render_template, url_for, flash, 
                   redirect, request, abort, Blueprint)
from app import db
from app.models import Posts
from app.posts.form import PostForm

posts = Blueprint('posts',__name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            post = Posts(title=form.title.data, content=form.content.data, user_id=current_user.id) # type: ignore
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created', 'success')
            return redirect(url_for('main.home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating post: {e}', 'danger')
            # Optionally, log the error here
    return render_template('create_post.html', title='New Post', 
                           form=form, legend='New Post')
        
@posts.route("/post/<int:post_id>")# type: ignore
def post(post_id):# type: ignore
    post = Posts.query.get_or_404(post_id)# type: ignore
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])# type: ignore
@login_required
def update_post(post_id):# type: ignore
    post = Posts.query.get_or_404(post_id)# type: ignore
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post Has been Updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id ))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        
    return render_template('create_post.html', title='Update Post', 
                           form=form, legend='Update Post')
    
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):# type: ignore
    post = Posts.query.get_or_404(post_id)# type: ignore
    if post.author != current_user:
        abort(403) 
    db.session.delete(post)
    db.session.commit()
    flash('Your Post Has Been Deleted!', 'success')
    return redirect(url_for('main.home'))
