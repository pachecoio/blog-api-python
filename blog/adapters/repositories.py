from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class AbstractRepository(ABC):
    session: Session = None

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def get(self, entity_id):
        pass

    @abstractmethod
    def get_all(self):
        pass


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, model, session):
        self.model = model
        self.session = session

    @property
    def query(self):
        return self.session.query(self.model)

    def add(self, entity):
        self.session.add(entity)
        return entity

    def get(self, entity_id):
        return self.query.get(entity_id)

    def get_all(self):
        return self.query

