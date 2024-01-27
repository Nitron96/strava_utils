import os
import json
import hashlib
import zipfile


CACHE_DIR = "cache"
HASH_ALGO = "sha1"


def check(identifier):
    return os.path.isfile(os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.json"))


def save(identifier, content):
    file_name = os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.json")
    with open(file_name, 'w') as f:
        json.dump(content, f)


def save_compressed(identifier, content):
    file_name = os.path.join(CACHE_DIR, f"{identifier}.zip")
    print(file_name)
    with zipfile.ZipFile(file_name, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.writestr("data.json", json.dumps(content).encode('utf-8'))


def save_test(identifier, content):
    file_name = os.path.join(CACHE_DIR, f"{identifier}.json")
    print(file_name)
    with open(file_name, 'w') as f:
        json.dump(content, f)


def load(identifier):
    file_name = os.path.join(CACHE_DIR, f"{cache_hash(identifier)}.json")
    # Maybe throw an error if cache file doesn't exist?
    if not check(cache_hash(identifier)):
        print(f"file not found {file_name}")
        pass
    with open(file_name) as f:
        data = json.load(f)
    return data


def load_test(identifier):
    file_name = os.path.join(CACHE_DIR, f"{identifier}.json")
    # Maybe throw an error if cache file doesn't exist?
    if not check(cache_hash(identifier)):
        print(f"file not found {file_name}")
        pass
    with open(file_name) as f:
        data = json.load(f)
    return data


def load_compressed_test(identifier):
    file_name = os.path.join(CACHE_DIR, f"{identifier}.zip")
    with zipfile.ZipFile(file_name, 'r') as zf:
        with zf.open("data.json", 'r') as f:
            data = json.load(f)
    return data


def cache_hash(identifier):
    return hashlib.new(HASH_ALGO, identifier.encode()).hexdigest()


os.makedirs(CACHE_DIR, exist_ok=True)

if __name__ == '__main__':
    CACHE_DIR = os.path.join("..", "cache")
    index = "f45f45337f2cba863acc7e22cce070bcff999a35"
    loaded_data = load_test(index)
    print(hash(str(loaded_data)))
    save_compressed(index, loaded_data)
    reloaded = load_compressed_test(index)
    print(hash(str(reloaded)))
