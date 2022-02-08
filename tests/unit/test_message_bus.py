from dataclasses import field, dataclass
from typing import Union, Dict, Type, List, Callable

import pytest

from blog.domain import commands
from blog.domain.commands import Command
from blog.services.handlers import create_user
from blog.services.unit_of_work import BlogUnitOfWork

Message = Union[Command]


@dataclass
class MessageBus:
    handlers: Dict[Type[Message], List[Callable]] = field(default_factory=dict)
    queue: [Message] = field(default_factory=list)

    def subscribe(self, event: Type[Message], fn: Callable):
        if event not in self.handlers:
            self.handlers[event] = [fn]
            return
        self.handlers[event].append(fn)

    def handle(self, message: Message):
        pass


@pytest.fixture
def uow(session_factory):
    return BlogUnitOfWork(session_factory)


def test_initial_message_bus_has_empty_queue():
    bus = MessageBus()
    assert not bus.queue


def test_initial_queue_has_no_command_handlers():
    bus = MessageBus()
    assert not bus.handlers


def test_has_commands_after_registering():
    bus = MessageBus()
    bus.subscribe(commands.CreateUser, create_user)
    assert commands.CreateUser in bus.handlers


# Todo
def test_trigger_callable():
    bus = MessageBus()
    bus.subscribe(commands.CreateUser, create_user)

    cmd = commands.CreateUser('Jon', 'Snow')
    bus.handle(cmd)
