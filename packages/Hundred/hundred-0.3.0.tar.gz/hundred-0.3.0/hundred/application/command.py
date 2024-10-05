from abc import ABC
from typing import Any

from injection import set_constant

from hundred.application.bus import Bus, SimpleBus, SubscriberDecorator
from hundred.application.dto import DTO


class Command(DTO, ABC): ...


type CommandBus[T] = Bus[Command, T]
command_handler: SubscriberDecorator[Command, Any] = SubscriberDecorator(CommandBus)

set_constant(SimpleBus(), CommandBus, alias=True)
