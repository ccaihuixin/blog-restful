from flask import current_app, render_template, url_for
from app.extensions import mail
from flask_mail import Message
from threading import Thread


def async_send_mail(app, msg):
    # 发邮件需要程序的上下文，否则发送不了邮件
    # 在新的线程中没有上下文，需要手动创建
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    # current_app代理代理对象中获取程序的原始实例
    app = current_app._get_current_object()
    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    msg.body = render_template(template + '.txt', **kwargs)
    print(msg.body)
    # print(url_for('user.activate', token=kwargs['token'], _external=True))
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr
