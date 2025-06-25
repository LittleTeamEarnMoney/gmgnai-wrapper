import redis
import json


class Redis:
    def __init__(self, config):
        redis_pool = redis.ConnectionPool(
            host=config["host"],
            port=config["port"],
            password=config["password"],
            decode_responses=True,
        )
        self.redis = redis.Redis(connection_pool=redis_pool)
        self.prefix = config["prefix"]

    def set_data(self, key, value, ex=60 * 60 * 24 * 30):
        key = self.generate_key(key)
        data_json = json.dumps(value)
        self.redis.set(name=key, value=data_json, ex=ex)

    def generate_key(self, key):
        return f"{self.prefix}{key}"

    def get_data(self, key):
        key = self.generate_key(key)
        data_json = self.redis.get(key)

        if data_json:
            data = json.loads(data_json)
            return data
        else:
            return None

    def del_data(self, key):
        key = self.generate_key(key)
        self.redis.delete(key)

    def get_all_data(self):
        data = self.redis.keys(f"{self.prefix}*")
        return data
