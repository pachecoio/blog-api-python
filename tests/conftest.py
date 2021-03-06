import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from blog.adapters.orm import start_mappers, metadata


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db):
    yield sessionmaker(bind=in_memory_db)


@pytest.fixture
def session(session_factory):
    start_mappers()
    yield session_factory()
    clear_mappers()
