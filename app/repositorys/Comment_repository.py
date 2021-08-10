import inject
from app.db import CommentSQL


class CommentRepository:

    def get_comment(self, **pk):
        return CommentSQL.session.query(CommentSQL.model).filter_by(**pk).order_by(
            CommentSQL.model.create_time.desc()).all()

    def get_comment_by_id(self, **pk):
        return CommentSQL.get(**pk)

    def create_comment(self, entity):
        CommentSQL.create(entity)

    def update_comment(self, id, entity):
        CommentSQL.update(id, entity)
