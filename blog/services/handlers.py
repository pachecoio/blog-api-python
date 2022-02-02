from dataclasses import asdict

from blog.domain import commands
from blog.domain.exceptions import (
    UserNotFoundException,
    ArticleNotFoundException,
    PermissionDeniedException,
)
from blog.domain.models import User, Article
from blog.services.unit_of_work import BlogUnitOfWork


def create_user(cmd: commands.CreateUser, uow: BlogUnitOfWork):
    with uow:
        user = User(**asdict(cmd))
        uow.users.add(user)
        uow.commit()
        return user.id


def add_article(
    cmd: commands.AddArticle,
    uow: BlogUnitOfWork
):
    with uow:
        user = uow.users.get(cmd.user_id)
        if not user:
            raise UserNotFoundException
        article = Article(
            cmd.title,
            cmd.description,
            cmd.content
        )
        user.add_article(article)
        uow.session.commit()
        return article.id


def publish_article(
    cmd: commands.PublishArticle,
    uow: BlogUnitOfWork
):
    with uow:
        article = uow.articles.get(cmd.article_id)
        if not article:
            raise ArticleNotFoundException(f"Article not found with id {cmd.article_id}")
        if article.user_id != cmd.user_id:
            raise PermissionDeniedException(
                f"User with {cmd.user_id} not allowed to change article {cmd.article_id}"
            )

        article.publish()
        uow.session.commit()


def delete_article(
    cmd: commands.DeleteArticle,
    uow: BlogUnitOfWork
):
    with uow:
        article = uow.articles.get(cmd.article_id)
        if not article:
            raise ArticleNotFoundException(f"Article not found with id {cmd.article_id}")
        if article.user_id != cmd.user_id:
            raise PermissionDeniedException(
                f"User with {cmd.user_id} not allowed to change article {cmd.article_id}"
            )
        article.delete()
        uow.session.commit()


def archive_article(
    cmd: commands.ArchiveArticle,
    uow: BlogUnitOfWork,
):
    with uow:
        article = uow.articles.get(cmd.article_id)
        if not article:
            raise ArticleNotFoundException(f"Article not found with id {cmd.article_id}")
        if article.user_id != cmd.user_id:
            raise PermissionDeniedException(
                f"User with {cmd.user_id} not allowed to change article {cmd.article_id}"
            )
        article.archive()
        uow.session.commit()
