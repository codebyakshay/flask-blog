from flask import Blueprint, render_template, request
from app.models import Posts
main = Blueprint('main',__name__)

@main.route("/home")
@main.route("/")
def home():
    page = request.args.get('page', 1, type = int)
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page = page, per_page=5)
    return render_template('home.html', posts=posts) # type: ignore

@main.route("/about")
def about():
    return render_template('about.html', title = 'About')
