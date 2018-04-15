# coding: utf8
import os
import redis

CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL') or 1)
REDIS_URL = os.getenv('REDIS_URL') or "redis://localhost:6379"
print(f"Redis URL: {REDIS_URL}")
REDIS = redis.from_url(REDIS_URL, decode_responses=True)
TIME_FORMAT = '%d-%m-%Y %H:%M:%S'
