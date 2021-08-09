import inject
from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.service import UserService
from app.forms import RegisterForm, LoginForm, PasswordForm, IconForm
from app.email import send_mail
from app.models import User
from app.extensions import db, photos, login_manager
from flask_login import login_user, logout_user, login_required, current_user
import os
from PIL import Image

user = Blueprint('user', __name__)

user_service = inject.instance(UserService)


@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # 创建对象，写入数据库
        u = User(username=form.username.data, password=form.password.data, email=form.email.data)
        user_service.register(u)
        token = u.generate_activate_token()
        # 发送激活邮件
        send_mail(form.email.data, '账户激活', 'email/account_activate', token=token, username=form.username.data)
        flash('激活邮件已发送，请点击连接完成用户激活')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/activate/<token>')
def activate(token):  # 新用户激活
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return redirect(url_for('user.login'))
    newuser = user_service.get_user(id=data.get('id'))
    if newuser is None:
        # 不存在此用户
        flash('账户激活失败')
        return redirect(url_for('main.index'))
    if not newuser.confirmed:
        # 账户没有激活时才激活
        newuser.confirmed = True
        user_service.update_user(id=newuser.id, entity=newuser.all_to_dict())
    flash('账户激活成功')
    return redirect(url_for('user.login'))


@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = user_service.get_user(username=form.username.data)  # 获取用户
        if u is None:
            flash('无效用户名')
        elif u.verify_password(form.password.data):
            # 验证通过，用户登录,顺便完成记住密码的功能
            login_user(u, remember=form.remember_me.data)
            # 如果有下一跳转到指定地址，没有跳转到首页
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('无效密码')
    return render_template('user/login.html', form=form)


# 回调根据id查询用户是谁 返回用户
@login_manager.user_loader
def loader_user(user_id):
    # return User.query.get(int(user_id))
    return user_service.get_user(id=int(user_id))


@user.route('/logout/')
# 保护路由
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))


@user.route('/profile/')
@login_required
def profile():
    return render_template('user/profile.html')


@user.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_pwd.data):
            current_user.password = form.new_pwd.data
            # db.session.add(current_user)
            user_service.update_user(id=current_user.id, entity=current_user.all_to_dict())
            flash('密码修改成功')
            return redirect(url_for('main.index'))
        else:
            flash('无效的原始密码')
            return redirect(url_for('user.change_password'))
    return render_template('user/change_password.html', form=form)


@user.route('/change_icon', methods=['GET', 'POST'])
def change_icon():
    form = IconForm()
    if form.validate_on_submit():
        # 生成随机文件名
        suffix = os.path.splitext(form.icon.data.filename)[1]
        name = rand_str() + suffix
        photos.save(form.icon.data, name=name)
        # 生成缩略图
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], name)
        img = Image.open(pathname)
        img.thumbnail((64, 64))
        img.save(pathname)
        # 删除原有头像
        if current_user.icon != 'default.jpg':
            # 第一次更换头像不删除，除此之外原来的头像都要删除
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
        # 保存新的头像
        current_user.icon = name
        # db.session.add(current_user)
        user_service.update_user(id=current_user.id, entity=current_user.all_to_dict())
        flash('头像已更换')
    return render_template('user/change_icon.html', form=form)


# 生成随机字符串
def rand_str(length=32):
    import random
    base_str = 'dfweafaegaergegewgegegergrgegewgaweg'
    return ''.join(random.choice(base_str) for i in range(length))
