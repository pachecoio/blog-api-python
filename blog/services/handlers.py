from blog.adapters.repositories import AbstractRepository
from blog.domain.exceptions import (
    UserNotFoundException,
    ArticleNotFoundException,
    PermissionDeniedException,
)
from blog.domain.models import User, Article
from blog.services.unit_of_work import BlogUnitOfWork


def create_user(uow: BlogUnitOfWork, first_name: str, last_name: str):
    with uow:
        user = User(first_name, last_name)
        uow.users.add(user)
        uow.commit()
        return user.id


def add_article(
    uow: BlogUnitOfWork, title: str, description: str, status: str, user_id: int
):
    with uow:
        user = uow.users.get(user_id)
        if not user:
            raise UserNotFoundException
        article = Article(
            title,
            description,
            status,
        )
        user.add_article(article)
        uow.session.commit()
        return article.id


def publish_article(
    uow: BlogUnitOfWork, article_id: str, user_id: int
):
    with uow:
        article = uow.articles.get(article_id)
        if not article:
            raise ArticleNotFoundException(f"Article not found with id {article_id}")
        if article.user_id != user_id:
            raise PermissionDeniedException(
                f"User with {user_id} not allowed to change article {article_id}"
            )

        article.publish()
        uow.session.commit()


def delete_article(
    uow: BlogUnitOfWork, article_id: str, user_id: int
):
    with uow:
        article = uow.articles.get(article_id)
        if not article:
            raise ArticleNotFoundException(f"Article not found with id {article_id}")
        if article.user_id != user_id:
            raise PermissionDeniedException(
                f"User with {user_id} not allowed to change article {article_id}"
            )
        article.delete()
        uow.session.commit()


def archive_article(
    uow: BlogUnitOfWork, article_id: str, user_id: int
):
    with uow:
        article = uow.articles.get(article_id)
        if not article:
            raise ArticleNotFoundException(f"Article not found with id {article_id}")
        if article.user_id != user_id:
            raise PermissionDeniedException(
                f"User with {user_id} not allowed to change article {article_id}"
            )
        article.archive()
        uow.session.commit()
