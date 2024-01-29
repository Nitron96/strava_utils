import os
import json
import hashlib
import zipfile
import logging


CACHE_DIR = "cache"
HASH_ALGO = "sha1"

CACHE_FALSE = 0
FILE_TRUE = 1
ZIP_TRUE = 2


# Ensure the cache dir is created when this package is imported
# Will need to only do this if cache type if disk based (not DynamoDB/other caching mechanism)
os.makedirs(CACHE_DIR, exist_ok=True)


def check(identifier):
    # Return truthy value for cache found falsy value for missed cache (and which type of cache)
    if os.path.isfile(os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.zip")):
        return ZIP_TRUE
    elif os.path.isfile(os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.json")):
        return FILE_TRUE
    else:
        return CACHE_FALSE


def save(identifier, content):
    # file_name = os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.json")
    # with open(file_name, 'w') as f:
    #     json.dump(content, f)
    file_name = os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.zip")
    logging.info(f"Saving {identifier} to cache as {file_name}")
    with zipfile.ZipFile(file_name, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.writestr("data.json", json.dumps(content).encode('utf-8'))


def load(identifier):
    # file_name = os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.json")
    # Maybe throw an error if cache file doesn't exist?
    cache_type = check(identifier)
    if not cache_type:
        print(f"Cache not found: {identifier}")
        pass
    elif cache_type == FILE_TRUE:
        with open(os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.json")) as f:
            data = json.load(f)
    elif cache_type == ZIP_TRUE:
        with zipfile.ZipFile(os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.zip"), 'r') as zf:
            with zf.open("data.json", 'r') as f:
                data = json.load(f)
    return data


def cache_hash(identifier):
    return hashlib.new(HASH_ALGO, identifier.encode()).hexdigest()
