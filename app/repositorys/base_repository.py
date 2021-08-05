class BaseRepository(object):
    def get(self, **pk):
        raise NotImplementedError

    def find(self, **keyd):
        raise NotImplementedError

    def update(self, entity):
        raise NotImplementedError

    def delete(self, entity):
        raise NotImplementedError

    def create(self, **kw):
        raise NotImplementedError

    def all(self):
        raise NotImplementedError


class SQLAlchemyReposotory(BaseRepository):
    def __init__(self, model, session):
        self.model = model
        self.session = session

    def get(self, **pk):
        return self.session.query(self.model).filter_by(**pk).one()

    def find(self, **keys):
        return self.session.query(self.model).filter_by(**keys).all()

    def update(self, **kwargs):
        self.session.query(self.model).filter_by(id=int(kwargs['id'])).update(**kwargs)
        self.session.commit()

    def all(self):
        return list(self.session.query(self.model).all())

    def create(self, entity):
        self.session.add(entity)
        self.session.commit()

    def delete(self, **pk):
        self.session.query(self.model).filter_by(**pk).delete()
        self.session.commit()