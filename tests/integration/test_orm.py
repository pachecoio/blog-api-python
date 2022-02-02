from sqlalchemy.orm import Session

from blog.domain.models import User, Article, get_new_uuid


def _create_user(session: Session, first_name: str, last_name: str):
    session.execute(
        "INSERT INTO users (first_name, last_name) VALUES "
        f"('{first_name}', '{last_name}')"
    )


def _create_article(session, title, description, content, user_id):
    id = get_new_uuid()
    session.execute(
        "INSERT INTO articles (id, title, description, content, status, user_id) VALUES "
        f"('{id}','{title}', '{description}', '{content}', 'draft', {user_id})"
    )


def test_can_retrieve_users(session):
    _create_user(session, 'Jon', 'Snow')
    users_query = session.query(User)
    assert users_query.count() == 1


def test_can_retrieve_articles(session):
    _create_user(session, 'Jon', 'Snow')
    user = session.query(User).first()
    _create_article(
        session,
        'Learning Python',
        'tips and tricks to work with python',
        'article content',
        user.id
    )
    articles_query = session.query(Article)
    assert articles_query.count() == 1
    article = articles_query.first()
    assert article.title == 'Learning Python'
    assert article.user_id == user.id
