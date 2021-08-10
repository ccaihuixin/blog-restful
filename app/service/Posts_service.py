import inject
from app.repositorys import PostsRepository


class PostsService:
    posts_repository = inject.attr(PostsRepository)

    def pagination(self, page=1, per_page=5, **kwargs):
        return self.posts_repository.pagination(page, per_page, **kwargs)

    def create_article(self, entity):
        self.posts_repository.create_article(entity=entity)

    def article_detail(self, **key):
        return self.posts_repository.article_detail(**key)

    def delete_article(self, **key):
        self.posts_repository.delete_article(**key)

    def update_article(self, id, entity):
        self.posts_repository.update_article(id, entity)

    def search_pagination(self,keyword,page,per_page):
        return self.posts_repository.search_pagination(keyword,page,per_page)
