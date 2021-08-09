import inject

from app.repositorys import UserRepository


class UserService:
    user_repository = inject.attr(UserRepository)

    def register(self, entity):  # 用户注册
        self.user_repository.create_user(entity)

    def get_user(self, **pk):  # 用户获取
        return self.user_repository.get_user(**pk)

    def update_user(self, id, entity):
        self.user_repository.update_user(id, entity)
