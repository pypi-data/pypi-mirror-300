from abc import ABC

from injection import set_constant

from hundred.application.bus import Bus, SubscriberDecorator, TaskBus
from hundred.application.dto import DTO


class Event(DTO, ABC): ...


type EventBus = Bus[Event, None]
event_handler: SubscriberDecorator[Event, None] = SubscriberDecorator(EventBus)

set_constant(TaskBus(), EventBus, alias=True)
