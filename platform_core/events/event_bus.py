from collections import defaultdict

from .event import Event
from .subscriber import Subscriber


class EventBus:
    def __init__(self):

        self._subscribers: dict[str, list[Subscriber]] = defaultdict(list)

    def subscribe(
        self,
        event_name: str,
        callback: Subscriber,
    ):

        self._subscribers[event_name].append(callback)

    def unsubscribe(
        self,
        event_name: str,
        callback: Subscriber,
    ):

        if callback in self._subscribers[event_name]:
            self._subscribers[event_name].remove(callback)

    def publish(self, event: Event):

        for callback in self._subscribers[event.name]:
            callback(event)
