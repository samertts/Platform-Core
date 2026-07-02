from collections.abc import Callable

from .event import Event

Subscriber = Callable[[Event], None]
