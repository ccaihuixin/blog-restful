from app.db import PostsSQL
import inject
class PostsRepository:
    PostsSQL=inject.attr(PostsSQL)
    def pagination(self,page=1,per_page=5,**kwargs):
        return PostsSQL.pagination(page=page,per_page=per_page,**kwargs)

