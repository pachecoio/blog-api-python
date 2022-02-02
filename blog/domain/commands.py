from dataclasses import dataclass


@dataclass
class Command:
    pass


@dataclass
class CreateUser(Command):
    first_name: str
    last_name: str


@dataclass
class AddArticle(Command):
    title: str
    description: str
    content: str
    user_id: int


@dataclass
class PublishArticle(Command):
    article_id: str
    user_id: int


@dataclass
class DeleteArticle(Command):
    article_id: str
    user_id: int


@dataclass
class ArchiveArticle(Command):
    article_id: str
    user_id: int
