from app.db import PostsSQL
import inject


class PostsRepository:

    def pagination(self, page=1, per_page=5, **kwargs):
        return PostsSQL.pagination(page=page, per_page=per_page, **kwargs)

    def create_article(self, entity):
        PostsSQL.create(entity)

    def article_detail(self, **key):
        return PostsSQL.get(**key)

    def delete_article(self, **key):
        PostsSQL.delete(**key)

    def update_article(self, id, entity):
        PostsSQL.update(id, entity)

    def search_pagination(self, keyword, page=1, per_page=5):
        return PostsSQL.search_pagination(keyword, page, per_page)
