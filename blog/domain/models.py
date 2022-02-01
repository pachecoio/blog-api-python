from dataclasses import field, dataclass
from datetime import datetime
from uuid import uuid1

from blog.domain.exceptions import InvalidStatusException


def get_new_uuid() -> str:
    return str(uuid1())


class ArticleStatus:
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    DELETED = 'deleted'


@dataclass
class Article:
    name: str
    description: str
    content: str
    status: str = ArticleStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    id: str = field(default_factory=get_new_uuid)

    def __eq__(self, other):
        return isinstance(other, Article) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def publish(self):
        if self.status != ArticleStatus.DRAFT:
            raise InvalidStatusException
        self.status = ArticleStatus.PUBLISHED

    def delete(self):
        if self.status != ArticleStatus.DRAFT:
            raise InvalidStatusException
        self.status = ArticleStatus.DELETED

    def archive(self):
        if self.status != ArticleStatus.PUBLISHED:
            raise InvalidStatusException
        self.status = ArticleStatus.ARCHIVED


@dataclass
class User:
    first_name: str
    last_name: str
    articles: [Article] = field(default_factory=set)

    def add_article(self, article):
        self.articles.add(article)
