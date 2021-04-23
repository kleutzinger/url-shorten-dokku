"""
connect to a redis database to map short urls to long urls
"""
import base64
import hashlib
import os

import redis
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
SHORT_URL_HASH_LENGTH = 5

red = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def check_long_url(long_url):
    "see if long url in db and return all long_url fields if so"
    long_url = "l:" + long_url
    if red.exists(long_url):
        return red.hgetall(long_url)
    else:
        return None


def check_short_url(short_url):
    "see if short url is in db and return long_url link if so"
    short_url = "s:" + short_url
    long_url = red.get(short_url)
    if long_url:
        return long_url
    return None


def hash_long_to_short(long_url):
    """
    turn a long input url into a short url's url-safe 5 character hash
    this is deterministic and the same long_url will always have the same hash
    """
    encoded = long_url.encode("utf-8")
    md5_hash = hashlib.md5(encoded).digest()
    return base64.urlsafe_b64encode(md5_hash)[:SHORT_URL_HASH_LENGTH]


def add_url_to_db(long_url, password=None):
    "process a long_url and input it into the db"
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
