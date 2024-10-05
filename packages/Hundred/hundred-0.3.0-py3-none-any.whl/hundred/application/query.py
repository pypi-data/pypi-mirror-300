from abc import ABC
from typing import Any

from injection import set_constant

from hundred.application.bus import Bus, SimpleBus, SubscriberDecorator
from hundred.application.dto import DTO


class Query(DTO, ABC): ...


type QueryBus[T] = Bus[Query, T]
query_handler: SubscriberDecorator[Query, Any] = SubscriberDecorator(QueryBus)

set_constant(SimpleBus(), QueryBus, alias=True)
