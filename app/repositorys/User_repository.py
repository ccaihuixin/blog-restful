import inject
from app.db import UserSQL


class UserRepository:

    def create_user(self, entity):
        UserSQL.create(entity=entity)

    def get_user(self, **pk):
        return UserSQL.get(**pk)

    def update_user(self, id, entity):
        UserSQL.update(id, entity)
