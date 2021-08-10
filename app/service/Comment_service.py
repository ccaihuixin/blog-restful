import inject

from app.repositorys import CommentRepository


class CommentService:
    comment_reposity = inject.attr(CommentRepository)

    def get_comment(self, **pk):
        return self.comment_reposity.get_comment(**pk)

    def get_comment_by_id(self, **pk):
        return self.comment_reposity.get_comment_by_id(**pk)

    def create_comment(self, entity):
        self.comment_reposity.create_comment(entity)

    def update_commnet(self, id, entity):
        self.comment_reposity.update_comment(id, entity)
