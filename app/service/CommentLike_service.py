import inject
from app.repositorys import CommentLikeRepository


class CommentLikeService:
    commentLike_Repository = inject.attr(CommentLikeRepository)

    def get_commentLike(self, **key):
        return self.commentLike_Repository.get_commentLike(**key)

    def create_commentLike(self,entity):
        self.commentLike_Repository.create_commentLike(entity)

    def delete_commentLike(self,**pk):
        self.commentLike_Repository.delete_commentLike(**pk)