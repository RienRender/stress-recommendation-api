import redis
import json


class RedisCache:

    def __init__(self):

        self.client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

    def get(self, key):

        value = self.client.get(key)

        if value:
            return json.loads(value)

        return None

    def set(self, key, value, ttl=300):

        self.client.setex(
            key,
            ttl,
            json.dumps(value)
        )