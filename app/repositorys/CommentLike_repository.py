from app.db import CommentLikeSQL


class CommentLikeRepository:
    def get_commentLike(self, **key):
        return CommentLikeSQL.find(**key)

    def create_commentLike(self, entity):
        CommentLikeSQL.create(entity)

    def delete_commentLike(self, **pk):
        CommentLikeSQL.delete(**pk)
