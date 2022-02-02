import pytest

from blog.adapters.repositories import SqlAlchemyRepository
from blog.domain import commands
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
from blog.services.unit_of_work import BlogUnitOfWork


@pytest.fixture
def user_repository(session):
    return SqlAlchemyRepository(User, session)


@pytest.fixture
def article_repository(session):
    return SqlAlchemyRepository(Article, session)


@pytest.fixture
def uow(session_factory):
    return BlogUnitOfWork(session_factory)


def test_create_user(user_repository, uow):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    assert user_id
    user = user_repository.get(user_id)
    assert user.first_name == "Jon"


def test_user_add_article(user_repository, uow):
    create_user_cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(create_user_cmd, uow)

    cmd = commands.AddArticle(
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    article_id = add_article(cmd, uow)
    assert article_id

    user = user_repository.get(user_id)
    assert len(user.articles)


def test_publish_article(uow, user_repository, article_repository):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    add_article_cmd = commands.AddArticle(
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    article_id = add_article(add_article_cmd, uow)

    cmd = commands.PublishArticle(article_id, user_id)
    publish_article(cmd, uow)
    article = article_repository.get(article_id)
    assert article.status == ArticleStatus.PUBLISHED


def test_raise_invalid_status_when_publishing_non_draft_article(
    uow, user_repository, article_repository
):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    add_article_cmd = commands.AddArticle(
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    article_id = add_article(add_article_cmd, uow)

    cmd = commands.PublishArticle(article_id, user_id)
    publish_article(cmd, uow)

    with pytest.raises(InvalidStatusException):
        publish_article(cmd, uow)


def test_raise_not_found_when_publishing_non_existing_article(
    uow, user_repository, article_repository
):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    fake_article_id = get_new_uuid()
    with pytest.raises(ArticleNotFoundException):
        cmd = commands.PublishArticle(fake_article_id, user_id)
        publish_article(cmd, uow)


def test_raise_permission_denied_when_publishing_article_by_different_user(
    uow, user_repository, article_repository
):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    add_article_cmd = commands.AddArticle(
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    article_id = add_article(add_article_cmd, uow)

    with pytest.raises(PermissionDeniedException):
        cmd = commands.PublishArticle(article_id, 123)
        publish_article(cmd, uow)


def test_delete_draft_article(uow, user_repository, article_repository):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    add_article_cmd = commands.AddArticle(
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    article_id = add_article(add_article_cmd, uow)

    cmd = commands.DeleteArticle(article_id, user_id)
    delete_article(cmd, uow)

    article = article_repository.get(article_id)
    assert article.status == ArticleStatus.DELETED


def test_raise_invalid_status_when_deleting_non_draft_article(
    uow, user_repository, article_repository
):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    add_article_cmd = commands.AddArticle(
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    article_id = add_article(add_article_cmd, uow)

    publish_article_cmd = commands.PublishArticle(article_id, user_id)
    publish_article(publish_article_cmd, uow)

    with pytest.raises(InvalidStatusException):
        cmd = commands.DeleteArticle(article_id, user_id)
        delete_article(cmd, uow)


def test_raise_permission_denied_when_deleting_article_by_different_user(
    uow, user_repository, article_repository
):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    add_article_cmd = commands.AddArticle(
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    article_id = add_article(add_article_cmd, uow)

    with pytest.raises(PermissionDeniedException):
        cmd = commands.DeleteArticle(article_id, 1231231)
        delete_article(cmd, uow)


def test_raise_not_found_when_deleting_non_existing_article(
    uow, user_repository, article_repository
):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    invalid_id = get_new_uuid()
    with pytest.raises(ArticleNotFoundException):
        cmd = commands.DeleteArticle(invalid_id, user_id)
        delete_article(cmd, uow)


def test_archive_article(uow, user_repository, article_repository):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    add_article_cmd = commands.AddArticle(
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    article_id = add_article(add_article_cmd, uow)
    publish_article_cmd = commands.PublishArticle(article_id, user_id)
    publish_article(publish_article_cmd, uow)

    cmd = commands.ArchiveArticle(article_id, user_id)
    archive_article(cmd, uow)
    article = article_repository.get(article_id)
    assert article.status == ArticleStatus.ARCHIVED


def test_raise_invalid_status_when_archiving_non_published_article(
    uow, user_repository, article_repository
):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    add_article_cmd = commands.AddArticle(
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    article_id = add_article(add_article_cmd, uow)

    with pytest.raises(InvalidStatusException):
        cmd = commands.ArchiveArticle(article_id, user_id)
        archive_article(cmd, uow)


def test_raise_permission_denied_when_archiving_article_by_different_user(
    uow, user_repository, article_repository
):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    add_article_cmd = commands.AddArticle(
        "Learning Python",
        "article description",
        "article content",
        user_id,
    )
    article_id = add_article(add_article_cmd, uow)
    publish_article_cmd = commands.PublishArticle(article_id, user_id)
    publish_article(publish_article_cmd, uow)

    invalid_user_id = 12312312
    with pytest.raises(PermissionDeniedException):
        cmd = commands.ArchiveArticle(article_id, invalid_user_id)
        archive_article(cmd, uow)


def test_raise_not_found_when_archiving_non_existing_article(
    uow, user_repository, article_repository
):
    cmd = commands.CreateUser('Jon', 'Snow')
    user_id = create_user(cmd, uow)

    invalid_article_id = get_new_uuid()
    with pytest.raises(ArticleNotFoundException):
        cmd = commands.ArchiveArticle(invalid_article_id, user_id)
        archive_article(cmd, uow)
