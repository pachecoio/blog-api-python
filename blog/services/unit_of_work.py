from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blog.adapters.repositories import SqlAlchemyRepository
from blog.config import get_database_uri
from blog.domain.models import User, Article


class AbstractUnitOfWork(ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(get_database_uri())
)


@dataclass
class BlogUnitOfWork(AbstractUnitOfWork):
    session_factory: sessionmaker = DEFAULT_SESSION_FACTORY

    def __enter__(self, *args):
        self.session = self.session_factory()
        self.users = SqlAlchemyRepository(User, self.session)
        self.articles = SqlAlchemyRepository(Article, self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
