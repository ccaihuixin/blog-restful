from flask import Flask, render_template
from app.config import config
from app.extensions import config_extensions
from app.api import config_blueprint
import inject

from app.models import CommentLike, Comment, User, Posts
from app.repositorys import SQLAlchemyReposotory, CommentLikeRepository, CommentRepository, UserRepository, \
    PostsRepository
from app.service import CommentLikeService, CommentService, UserService, PostsService
import app.db


def create_app(config_name):
    # 创建应用实例
    app = Flask(__name__)
    # 初始化配置
    app.config.from_object(config[config_name])  # 传类名
    # 调用初始化函数
    config[config_name].init_app(app)
    # 配置相关扩展
    config_extensions(app)
    # 注册蓝本
    inject.configure(config_ioc)
    config_blueprint(app)
    # 配置错误显示
    config_errorhandler(app)
    # 返回应用实例
    return app


def config_errorhandler(app):
    @app.errorhandler(404)
    def page_not_fount(e):
        return render_template('errors/404.html')


def config_ioc(binder):
    session = extensions.db.session
    CommentLikeSQL = db.CommentLikeSQL.init_SQLAlchemyReposotory(CommentLike, session)
    CommentSQL = db.CommentSQL.init_SQLAlchemyReposotory(Comment, session)
    UserSQL = db.UserSQL.init_SQLAlchemyReposotory(User, session)
    PostsSQL = db.PostsSQL.init_SQLAlchemyReposotory(Posts, session)

    Comment_repository = CommentRepository()
    CommentLike_repository = CommentLikeRepository()
    User_repository = UserRepository()
    Posts_repository = PostsRepository()

    Comment_service = CommentService()
    CommentLike_service = CommentLikeService()
    User_service = UserService()
    Posts_service = PostsService()

    binder.bind(db.CommentLikeSQL, CommentLikeSQL)
    binder.bind(db.CommentSQL, CommentSQL)
    binder.bind(db.UserSQL, UserSQL)
    binder.bind(db.PostsSQL, PostsSQL)

    binder.bind(CommentRepository, Comment_repository)
    binder.bind(CommentLikeRepository, CommentLike_repository)
    binder.bind(UserRepository, User_repository)
    binder.bind(PostsRepository, Posts_repository)

    binder.bind(CommentService, Comment_service)
    binder.bind(CommentLikeService, CommentLike_service)
    binder.bind(UserService, User_service)
    binder.bind(PostsService, Posts_service)
