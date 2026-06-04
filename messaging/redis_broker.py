import json

import redis

from messaging.base import MessageBroker


class RedisBroker(MessageBroker):

    def __init__(self, url: str):
        self.client = redis.from_url(url)

    def publish(self, event: str, data: dict) -> None:
        self.client.publish(event, json.dumps(data))