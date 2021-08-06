import inject
from app.repositorys import PostsRepository


class PostsService:
    posts_repository = inject.attr(PostsRepository)

    def pagination(self, page=1, per_page=5, **kwargs):
        return self.posts_repository.pagination(page, per_page, **kwargs)
