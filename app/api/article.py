from flask import Blueprint, render_template, url_for, redirect, request, jsonify, current_app
from app.forms import PostsForm, ChangePostsForm
from flask_login import login_required, current_user
from app.models import Posts, Comment,CommentLike
from app.extensions import db
from datetime import datetime
from app.response_code import RET

article = Blueprint('article', __name__)


@article.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    form = PostsForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            u = current_user._get_current_object()  # 获取原来的user对象
            p = Posts(title=form.title.data, describe=form.content.data[0:145] + '……', content=form.content.data,
                      user=u)
            # 添加进入数据库
            db.session.add(p)
            return redirect(url_for("main.index"))
    return render_template('article/publish.html', form=form)


@article.route('/mypublish', methods=['GET'])
@login_required
def mypublish():
    u = current_user._get_current_object()  # 获取原来的user对象
    page = request.args.get('page', 1, type=int)  # 获取请求中的分页的页码，默认是第一页并转换为int
    pagination = Posts.query.filter_by(uid=u.id).order_by(Posts.timestamp.desc()).paginate(page,
                                                                                           per_page=5)  # err_out 不打印错误信息
    posts = pagination.items
    return render_template('article/mypublish.html', posts=posts, pagination=pagination)


@article.route('/article_detail', methods=['GET'])
def article_detail():
    id = request.args.get('id')
    posts = Posts.query.filter_by(id=id).first()
    comments = Comment.query.filter(Comment.post_id == id).order_by(Comment.create_time.desc()).all()
    # 1.根据新闻编号,查询新闻对象
    # 6.查询数据库中,该新闻的所有评论内容
    try:
        comments = Comment.query.filter(Comment.post_id == id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取评论失败")

    # 6.1 用户点赞过的评论编号
    try:
        # 6.1.1 该用户点过所有的赞
        commentlikes = []
        if current_user.is_authenticated:
            commentlikes = CommentLike.query.filter(CommentLike.user_id == current_user._get_current_object().id).all()

        # 6.1.2获取用户所有点赞过的评论编号
        mylike_comment_ids = []
        for commentLike in commentlikes:
            mylike_comment_ids.append(commentLike.comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取点赞失败")

    # 7.将评论的对象列表, 转成字典列表
    comments_list = []
    for comment in comments:
        # 将评论对象,转字典
        comm_dict = comment.to_dict()

        # 添加is_like记录点赞
        comm_dict["is_like"] = False

        # 判断用户是否有对评论点过赞
        if current_user.is_authenticated and comment.id in mylike_comment_ids:
            comm_dict["is_like"] = True

        comments_list.append(comm_dict)

    # 2.携带数据,渲染页面
    data = {
        "posts": posts.to_dict(),
        "user": current_user._get_current_object().to_dict() if current_user.is_authenticated else "",
        "comments": comments_list,
    }
    return render_template('article/article_detail.html', data=data)


@article.route('/article_delete', methods=['GET'])
@login_required
def article_delete():
    id = request.args.get('id')
    result = Posts.query.filter_by(id=id).delete()
    if result is not None:
        return redirect(url_for('article.mypublish'))


@article.route('/article_change', methods=['GET', 'POST'])
@login_required
def article_change():
    form = ChangePostsForm()
    if request.method == 'GET':
        id = request.args.get('id')
        posts = Posts.query.filter_by(id=id).first()
        form.id.data = posts.id
        form.title.data = posts.title
        form.content.data = posts.content
        return render_template('article/publish.html', form=form)
    else:
        if form.validate_on_submit():
            id = Posts.query.filter_by(id=form.id.data).update(
                {"title": form.title.data, "content": form.content.data, "describe": form.content.data[0:145] + '……',
                 "timestamp": datetime.utcnow()})
            return redirect(url_for("article.mypublish"))


@article.route('/article_search', methods=['GET'])
def article_search():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter(Posts.title.like('%{keyword}%'.format(keyword=keyword))).order_by(
        Posts.timestamp.desc()).paginate(page, per_page=5)
    posts = pagination.items
    print(posts)
    return render_template('article/search.html', posts=posts, pagination=pagination, keyword=keyword)


# 新闻评论后端
# 请求路径: /news/news_comment
# 请求方式: POST
# 请求参数:news_id,comment,parent_id, g.user
# 返回值: errno,errmsg,评论字典
@article.route('/article_comment', methods=['POST'])
@login_required
def article_comment():
    """
    1. 判断用户是否登陆
    2. 获取请求参数
    3. 校验参数,为空校验
    4. 根据新闻编号取出新闻对象,判断新闻是否存在
    5. 创建评论对象,设置属性
    6. 保存评论对象到数据库中
    7. 返回响应,携带评论的数据
    :return:
    """
    # 1. 判断用户是否登陆
    if not current_user.is_authenticated:
        return jsonify(errno='RET.NODATA', errmsg="用户未登录")

    # 2. 获取请求参数
    post_id = request.json.get("post_id")
    content = request.json.get("comment")
    parent_id = request.json.get("parent_id")
    print(post_id)
    print(content)
    print(parent_id)
    # 3. 校验参数,为空校验
    if not all([post_id, content]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    # 4. 根据新闻编号取出新闻对象,判断新闻是否存在
    try:
        post = Posts.query.get(post_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取新闻失败")

    if not post: return jsonify(errno=RET.NODATA, errmsg="新闻不存在")

    # 5. 创建评论对象,设置属性
    comment = Comment()
    comment.user_id = current_user._get_current_object().id
    comment.post_id = post_id
    comment.content = content
    if parent_id:
        comment.parent_id = parent_id

    # 6. 保存评论对象到数据库中
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="评论失败")

    # 7. 返回响应,携带评论的数据
    return jsonify(errno=RET.OK, errmsg="评论成功", data=comment.to_dict())

# 评论点赞
# 请求路径: /news/comment_like
# 请求方式: POST
# 请求参数:news_id,comment_id,action,g.user
# 返回值: errno,errmsg
@article.route('/comment_like', methods=['POST'])
@login_required
def comment_like():
    """
    1. 判断用户是否有登陆
    2. 获取参数
    3. 参数校验,为空校验
    4. 操作类型进行校验
    5. 通过评论编号查询评论对象,并判断是否存在
    6. 根据操作类型点赞取消点赞
    7. 返回响应
    :return:
    """
    # 1. 判断用户是否有登陆
    if not current_user.is_authenticated:
        return jsonify(errno=RET.NODATA, errmsg="用户未登录")

    # 2. 获取参数
    comment_id = request.json.get("comment_id")
    action = request.json.get("action")

    # 3. 参数校验,为空校验
    if not all([comment_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    # 4. 操作类型进行校验
    if not action in ["add", "remove"]:
        return jsonify(errno=RET.DATAERR, errmsg="操作类型有误")

    # 5. 通过评论编号查询评论对象,并判断是否存在
    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取评论失败")

    if not comment: return jsonify(errno=RET.NODATA, errmsg="评论不存在")

    # 6. 根据操作类型点赞取消点赞
    try:
        if action == "add":
            # 6.1 判断用户是否有对该评论点过赞
            comment_like = CommentLike.query.filter(CommentLike.user_id == current_user._get_current_object().id,
                                                    CommentLike.comment_id == comment_id).first()
            if not comment_like:
                # 创建点赞对象
                comment_like = CommentLike()
                comment_like.user_id = current_user._get_current_object().id
                comment_like.comment_id = comment_id

                # 添加到数据库中
                db.session.add(comment_like)

                # 将该评论的点赞数量+1
                comment.like_count += 1
                db.session.commit()
        else:
            # 6.2 判断用户是否有对该评论点过赞
            comment_like = CommentLike.query.filter(CommentLike.user_id == current_user._get_current_object().id,
                                                    CommentLike.comment_id == comment_id).first()
            if comment_like:
                # 删除点赞对象
                db.session.delete(comment_like)

                # 将该评论的点赞数量1
                if comment.like_count > 0:
                    comment.like_count -= 1
                db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="操作失败")

    # 7. 返回响应
    return jsonify(errno=RET.OK, errmsg="操作成功")
