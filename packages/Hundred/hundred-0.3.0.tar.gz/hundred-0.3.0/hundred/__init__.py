from pathlib import Path
from typing import Final

from .application.command import Command, CommandBus, command_handler
from .application.dto import DTO
from .application.event import Event, EventBus, event_handler
from .application.middleware import Middleware, MiddlewareResult
from .application.query import Query, QueryBus, query_handler
from .domain.entity import Aggregate, Entity
from .domain.vo import ValueObject

__all__ = (
    "DIRECTORY",
    "Aggregate",
    "Command",
    "CommandBus",
    "DTO",
    "Entity",
    "Event",
    "EventBus",
    "Middleware",
    "MiddlewareResult",
    "Query",
    "QueryBus",
    "ValueObject",
    "command_handler",
    "event_handler",
    "query_handler",
)

DIRECTORY: Final[Path] = Path(__file__).resolve().parent
