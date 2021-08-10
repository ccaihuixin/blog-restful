from datetime import datetime

from app.extensions import db


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    describe = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    rid = db.Column(db.Integer, index=True, default=0)  # 回复id 默认为0 表示发表
    # 指定外键(表名.字段)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship("Comment", lazy="dynamic")

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "describe": self.describe,
            "create_time": self.timestamp,
            "content": self.content,
            "comments_count": self.comments.count(),
            "author": self.user.to_dict() if self.user else None
        }
        return resp_dict

    def update_dict(self):
        resp_dict = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'describe': self.describe,
            'timestamp': self.timestamp,
        }
        return resp_dict
