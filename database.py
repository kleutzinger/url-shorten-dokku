"""
input a long url

storing:

map short urls to long urls

"""
import base64
import hashlib
import os

import redis
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

red = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def check_long_url(long_url):
    long_url = "l:" + long_url
    if red.exists(long_url):
        return red.hgetall(long_url)
    else:
        return None


def check_short_url(short_url):
    short_url = "s:" + short_url
    long_url = red.get(short_url)
    if long_url:
        return long_url
    return None


def hash_long_to_short(long_url):
    LEN = 5
    encoded = long_url.encode("utf-8")
    return base64.urlsafe_b64encode((hashlib.md5(encoded).digest()))[:LEN]


def add_url_to_db(long_url, password=None):
    "also add salt"
    pre_existing = red.hgetall("l:" + long_url)
    if pre_existing:
        print("already added")
        return pre_existing
    short_hash = hash_long_to_short(long_url).decode()
    salt = base64.urlsafe_b64encode(os.urandom(20)).decode()[:5]
    insert = {"short_hash": short_hash, "salt": salt, "pw_hash": ""}
    red.hset("l:" + long_url, mapping=insert)
    red.set("s:" + short_hash, long_url)
    return insert
