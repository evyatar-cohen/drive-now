from abc import ABC, abstractmethod


class MessageBroker(ABC):

    @abstractmethod
    def publish(self, event: str, data: dict) -> None: ...