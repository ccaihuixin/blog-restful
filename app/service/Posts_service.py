import inject
from app.repositorys import PostsRepository


class PostsService:
    posts_repository = inject.attr(PostsRepository)

    def pagination(self, page=1, per_page=5, **kwargs):
        self.posts_repository
