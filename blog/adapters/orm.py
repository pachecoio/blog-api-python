from sqlalchemy import MetaData, Table, Column, Integer, String, Unicode, ForeignKey, DateTime
from sqlalchemy.orm import mapper, relationship

from blog.domain.models import User, Article

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
)

articles = Table(
    'articles',
    metadata,
    Column('id', Unicode, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=False),
    Column('content', String, nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('created_at', DateTime, nullable=String),
    Column('updated_at', DateTime, nullable=String),
)


def start_mappers():
    articles_mappers = mapper(Article, articles)
    users_mapper = mapper(User, users, properties={
        'articles': relationship(articles_mappers, collection_class=set)
    })
