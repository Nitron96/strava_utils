import os
import json
import hashlib


CACHE_DIR = "cache"
HASH_ALGO = "sha1"


def check(identifier):
    return os.path.isfile(os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.json"))


def save(identifier, content):
    file_name = os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.json")
    with open(file_name, 'w') as f:
        json.dump(content, f)


def load(identifier):
    file_name = os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.json")
    # Maybe throw an error if cache file doesn't exist?
    if not check(cache_hash(identifier)):
        pass
    with open(file_name) as f:
        data = json.load(f)
    return data


def cache_hash(identifier):
    return hashlib.new(HASH_ALGO, identifier.encode()).hexdigest()


os.makedirs(CACHE_DIR, exist_ok=True)
