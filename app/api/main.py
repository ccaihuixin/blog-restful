from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from app.forms import PostsForm
from app.models import Posts
from app.extensions import db
from app.service import PostsService
import inject

main = Blueprint('main', __name__)
from flask_login import current_user

posts_service = inject.instance(PostsService)


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    # pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=5)

    posts = pagination.items
    return render_template('main/index.html', posts=posts, pagination=pagination)
