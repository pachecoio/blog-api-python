from blog.adapters.repositories import SqlAlchemyRepository
from blog.domain.models import User, Article


def test_add_and_retrieve_users(session):
    repo = SqlAlchemyRepository(
        model=User,
        session=session
    )
    user = User('Jon', 'Snow')
    repo.add(user)
    session.commit()

    users = repo.get_all()
    assert users.count() == 1


def test_add_and_retrieve_user_articles(session):
    user_repository = SqlAlchemyRepository(
        model=User,
        session=session
    )
    user_repository.add(User('Jon', 'Snow'))
    user = user_repository.get_all().first()
    assert not len(user.articles)

    article = Article(
        'Learning Python',
        'article description',
        'article content',
    )
    user.add_article(article)
    session.commit()

    user = user_repository.get_all().first()
    assert article in user.articles
