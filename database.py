"""

"""
import redis
import os
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

red = redis.Redis.from_url(REDIS_URL)


def check_long_url(long_url):
    pass


def check_short_url(short_url):
    pass


def add_url(long_url, password=None):
    "also add salt"
    pass


def delete_url(password):
    "check existence and against salt"
    pass
