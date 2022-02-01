import pytest

from blog.adapters.repositories import SqlAlchemyRepository
from blog.domain.models import User, Article, ArticleStatus
from blog.services.handlers import create_user, add_article, publish_article


@pytest.fixture
def user_repository(session):
    return SqlAlchemyRepository(User, session)


@pytest.fixture
def article_repository(session):
    return SqlAlchemyRepository(Article, session)


def test_create_user(user_repository, session):
    user_id = create_user(user_repository, 'Jon', 'Snow')

    assert user_id
    user = user_repository.get(user_id)
    assert user.first_name == 'Jon'


def test_user_add_article(user_repository, session):
    user_id = create_user(user_repository, 'Jon', 'Snow')

    article_id = add_article(
        user_repository,
        'Learning Python',
        'article description',
        'article content',
        user_id
    )
    assert article_id

    user = user_repository.get(user_id)
    assert len(user.articles)


def test_publish_article(user_repository, article_repository):
    user_id = create_user(user_repository, 'Jon', 'Snow')

    article_id = add_article(
        user_repository,
        'Learning Python',
        'article description',
        'article content',
        user_id
    )

    publish_article(
        article_repository,
        article_id,
        user_id
    )

    article = article_repository.get(article_id)
    assert article.status == ArticleStatus.PUBLISHED

