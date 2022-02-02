import pytest

from blog.adapters.repositories import SqlAlchemyRepository
from blog.domain.exceptions import (
    InvalidStatusException,
    PermissionDeniedException,
    ArticleNotFoundException,
)
from blog.domain.models import User, Article, ArticleStatus, get_new_uuid
from blog.services.handlers import (
    create_user,
    add_article,
    publish_article,
    delete_article,
    archive_article,
)


@pytest.fixture
def user_repository(session):
    return SqlAlchemyRepository(User, session)


@pytest.fixture
def article_repository(session):
    return SqlAlchemyRepository(Article, session)


def test_create_user(user_repository, session):
    user_id = create_user(user_repository, "Jon", "Snow")

    assert user_id
    user = user_repository.get(user_id)
    assert user.first_name == "Jon"


def test_user_add_article(user_repository, session):
    user_id = create_user(user_repository, "Jon", "Snow")

    article_id = add_article(
        user_repository,
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    assert article_id

    user = user_repository.get(user_id)
    assert len(user.articles)


def test_publish_article(user_repository, article_repository):
    user_id = create_user(user_repository, "Jon", "Snow")

    article_id = add_article(
        user_repository,
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )

    publish_article(article_repository, article_id, user_id)
    article = article_repository.get(article_id)
    assert article.status == ArticleStatus.PUBLISHED


def test_raise_invalid_status_when_publishing_non_draft_article(
    user_repository, article_repository
):
    user_id = create_user(user_repository, "Jon", "Snow")

    article_id = add_article(
        user_repository,
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )

    publish_article(article_repository, article_id, user_id)

    with pytest.raises(InvalidStatusException):
        publish_article(article_repository, article_id, user_id)


def test_raise_not_found_when_publishing_non_existing_article(
    user_repository, article_repository
):
    user_id = create_user(user_repository, "Jon", "Snow")

    fake_article_id = get_new_uuid()
    with pytest.raises(ArticleNotFoundException):
        publish_article(article_repository, fake_article_id, user_id)


def test_raise_permission_denied_when_publishing_article_by_different_user(
    user_repository, article_repository
):
    user_id = create_user(user_repository, "Jon", "Snow")

    article_id = add_article(
        user_repository,
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )

    with pytest.raises(PermissionDeniedException):
        publish_article(article_repository, article_id, 123)


def test_delete_draft_article(user_repository, article_repository):
    user_id = create_user(user_repository, "Jon", "Snow")
    article_id = add_article(
        user_repository,
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )

    delete_article(article_repository, article_id, user_id)

    article = article_repository.get(article_id)
    assert article.status == ArticleStatus.DELETED


def test_raise_invalid_status_when_deleting_non_draft_article(
    user_repository, article_repository
):
    user_id = create_user(user_repository, "Jon", "Snow")
    article_id = add_article(
        user_repository,
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )

    publish_article(
        article_repository,
        article_id,
        user_id,
    )

    with pytest.raises(InvalidStatusException):
        delete_article(article_repository, article_id, user_id)


def test_raise_permission_denied_when_deleting_article_by_different_user(
    user_repository, article_repository
):
    user_id = create_user(user_repository, "Jon", "Snow")
    article_id = add_article(
        user_repository,
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )

    with pytest.raises(PermissionDeniedException):
        delete_article(article_repository, article_id, 12312321)


def test_raise_not_found_when_deleting_non_existing_article(
    user_repository, article_repository
):
    user_id = create_user(user_repository, "Jon", "Snow")
    invalid_id = get_new_uuid()
    with pytest.raises(ArticleNotFoundException):
        delete_article(
            article_repository,
            invalid_id,
            user_id,
        )


def test_archive_article(user_repository, article_repository):
    user_id = create_user(user_repository, "Jon", "Snow")
    article_id = add_article(
        user_repository,
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    publish_article(
        article_repository,
        article_id,
        user_id,
    )

    archive_article(article_repository, article_id, user_id)
    article = article_repository.get(article_id)
    assert article.status == ArticleStatus.ARCHIVED


def test_raise_invalid_status_when_archiving_non_published_article(
    user_repository, article_repository
):
    user_id = create_user(user_repository, "Jon", "Snow")
    article_id = add_article(
        user_repository,
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )

    with pytest.raises(InvalidStatusException):
        archive_article(article_repository, article_id, user_id)


def test_raise_permission_denied_when_archiving_article_by_different_user(
    user_repository, article_repository
):
    user_id = create_user(user_repository, "Jon", "Snow")
    article_id = add_article(
        user_repository,
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    publish_article(
        article_repository,
        article_id,
        user_id,
    )

    invalid_user_id = 12312312
    with pytest.raises(PermissionDeniedException):
        archive_article(article_repository, article_id, invalid_user_id)


def test_raise_not_found_when_archiving_non_existing_article(
    user_repository, article_repository
):
    user_id = create_user(user_repository, "Jon", "Snow")

    invalid_article_id = 12312312
    with pytest.raises(ArticleNotFoundException):
        archive_article(article_repository, invalid_article_id, user_id)
