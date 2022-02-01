from blog.adapters.repositories import AbstractRepository
from blog.domain.exceptions import UserNotFoundException, ArticleNotFoundException, PermissionDeniedException
from blog.domain.models import User, Article


def create_user(repository: AbstractRepository, first_name: str, last_name: str):
    user = User(first_name, last_name)
    repository.add(user)
    repository.session.commit()
    return user.id


def add_article(
    user_repository: AbstractRepository,
    title: str,
    description: str,
    status: str,
    user_id: int
):
    user = user_repository.get(user_id)
    if not user:
        raise UserNotFoundException
    article = Article(
        title,
        description,
        status,
    )
    user.add_article(article)
    user_repository.session.commit()
    return article.id


def publish_article(
    article_repository: AbstractRepository,
    article_id: str,
    user_id: int
):
    article = article_repository.get(article_id)
    if not article:
        raise ArticleNotFoundException(
            f'Article not found with id {article_id}'
        )
    if article.user_id != user_id:
        raise PermissionDeniedException(
            f'User with {user_id} not allowed to change article {article_id}'
        )

    article.publish()
    article_repository.session.commit()

