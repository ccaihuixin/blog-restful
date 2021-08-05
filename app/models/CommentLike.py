from datetime import datetime
from app.extensions import db
class CommentLike(db.Model):
    """评论点赞"""
    __tablename__ = "comment_like"
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间
    comment_id = db.Column("comment_id", db.Integer, db.ForeignKey("comment.id"), primary_key=True)  # 评论编号
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True)  # 用户编号