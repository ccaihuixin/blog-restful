from flask import Blueprint, render_template, current_app, flash, redirect, url_for, request
from app.forms import PostsForm
from app.models import Posts
from app.extensions import db
from app.service import PostsService
import inject

main = Blueprint('main', __name__)
from flask_login import current_user




@main.route('/', methods=['GET', 'POST'])
def index():
    posts_service = inject.instance(PostsService)
    page = request.args.get('page', 1, type=int)
    pagination = posts_service.pagination(page, per_page=5, rid=0)
    posts = pagination.items
    return render_template('main/index.html', posts=posts, pagination=pagination)
