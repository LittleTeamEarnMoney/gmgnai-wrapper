import time
import random

from gmgn import gmgn
from db import Redis
from loguru import logger


# redis配置
REDIS_CONFIG = {
    "host": "127.0.0.1",
    "port": "1233",
    "password": None,
    # 数据有效期，以下为30天
    "ex": 60 * 60 * 24 * 30,
    "prefix": "gmgn",
}

if __name__ == "__main__":
    gmgn = gmgn()
    redis = Redis(REDIS_CONFIG)
    while True:
        try:
            pairs = gmgn.getNewPairs(limit=random.randint(700, 1000))
            for pair in pairs["pairs"]:
                redis.set_data(key=pair["base_address"], value=pair, ex=REDIS_CONFIG["ex"])
                # logger.info(f"New Pair: {pair['base_address']}")
            logger.info(f"New Pairs: {len(pairs['pairs'])}")
        except Exception as e:
            logger.error(e)

        time.sleep(random.randint(1, 4))
