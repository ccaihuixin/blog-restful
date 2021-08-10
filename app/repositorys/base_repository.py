class BaseRepository(object):
    def get(self, **pk):
        raise NotImplementedError

    def find(self, **keyd):
        raise NotImplementedError

    def update(self, **kwargs):
        raise NotImplementedError

    def delete(self, **pk):
        raise NotImplementedError

    def create(self, entity):
        raise NotImplementedError

    def all(self):
        raise NotImplementedError

    def pagination(self, page=1, per_page=5, **kwargs):
        raise NotImplementedError


class SQLAlchemyReposotory(BaseRepository):
    def __init__(self):
        pass

    def init_SQLAlchemyReposotory(self, model, session):
        self.model = model
        self.session = session

    def get(self, **pk):
        return self.session.query(self.model).filter_by(**pk).first()

    def find(self, **keys):
        return self.session.query(self.model).filter_by(**keys).all()

    def find_and_sort_by_time(self, **keys):
        return self.session.query(self.model).filter_by(**keys).order_by(self.model.create_time.desc()).all()

    def update(self, id, entity):
        self.session.query(self.model).filter_by(id=id).update(entity)
        self.session.commit()

    def all(self):
        return list(self.session.query(self.model).all())

    def create(self, entity):
        self.session.add(entity)
        self.session.commit()

    def delete(self, **pk):
        self.session.query(self.model).filter_by(**pk).delete()
        self.session.commit()

    def pagination(self, page=1, per_page=5, **kwargs):
        pagination = self.session.query(self.model).filter_by(**kwargs).order_by(
            self.model.timestamp.desc()).paginate(page, per_page=5)
        return pagination

    def search_pagination(self, keyword, page=1, per_page=5):
        pagination = self.session.query(self.model).filter(
            self.model.title.like('%{keyword}%'.format(keyword=keyword))).order_by(
            self.model.timestamp.desc()).paginate(page, per_page=per_page)
        return pagination
