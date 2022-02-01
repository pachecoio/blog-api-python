import pytest

from blog import __version__
from blog.domain.exceptions import InvalidStatusException
from blog.domain.models import Article, ArticleStatus, User


def test_version():
    assert __version__ == "0.1.0"


def test_create_article_instance():
    article = Article(
        "Learning python",
        "Tips and tricks working with python",
        content="content",
    )

    assert article.status == ArticleStatus.DRAFT


def test_publish_article():
    article = Article(
        "Learning python",
        "Tips and tricks working with python",
        content="content",
    )
    article.publish()
    assert article.status == ArticleStatus.PUBLISHED


def test_raise_invalid_status_when_publish_article_already_published():
    article = Article(
        "Learning python",
        "Tips and tricks working with python",
        content="content",
        status=ArticleStatus.PUBLISHED,
    )
    with pytest.raises(InvalidStatusException):
        article.publish()


def test_delete_draft_article():
    article = Article(
        "Learning python",
        "Tips and tricks working with python",
        content="content",
    )
    article.delete()
    assert article.status == ArticleStatus.DELETED


def test_raise_invalid_status_when_delete_non_draft_article():
    article = Article(
        "Learning python",
        "Tips and tricks working with python",
        content="content",
        status=ArticleStatus.PUBLISHED,
    )
    with pytest.raises(InvalidStatusException):
        article.delete()


def test_archive_published_status():
    article = Article(
        "Learning python",
        "Tips and tricks working with python",
        content="content",
        status=ArticleStatus.PUBLISHED,
    )
    article.archive()
    assert article.status == ArticleStatus.ARCHIVED


def test_raise_invalid_status_when_archiving_non_published_article():
    article = Article(
        "Learning python",
        "Tips and tricks working with python",
        content="content",
        status=ArticleStatus.DRAFT,
    )
    with pytest.raises(InvalidStatusException):
        article.archive()


def test_new_user_has_no_articles():
    user = User("Jon", "Snow")
    assert not user.articles


def test_user_add_article():
    article = Article(
        "Learning python", "Tips and tricks working with python", content="content"
    )
    user = User("Jon", "Snow")
    user.add_article(article)
    assert article in user.articles
