import glob
import hashlib
import os
from pathlib import Path
from typing import Union

from platformdirs import user_cache_dir

CACHED_HASHES = {}
CACHE_DIR = Path(user_cache_dir(appname="rhymek"))

CACHE_DIR.mkdir(parents=True, exist_ok=True)


def stable_hash(obj: str) -> str:
    sha1_hash = hashlib.sha1()
    sha1_hash.update(obj.encode())
    return sha1_hash.hexdigest()


def populate_cached_hashes():
    global CACHED_HASHES
    for filepath in glob.glob(os.path.join(CACHE_DIR, "*.cache")):
        CACHED_HASHES[Path(filepath).stem] = os.path.abspath(filepath)


def get_cache(word_in: str, langcode: str) -> Union[None, list[str]]:
    global CACHED_HASHES
    current_operation_hash = stable_hash(f"{langcode}__{word_in}")
    cache_path = CACHED_HASHES.get(current_operation_hash, None)

    if cache_path == None:
        return None

    return open(cache_path, "r", encoding="utf8").read().split("\n")


def set_cache(word_in: str, langcode: str, results: list[str]):
    global CACHED_HASHES
    current_operation_hash = stable_hash(f"{langcode}__{word_in}")
    with open(
        os.path.join(CACHE_DIR, f"{current_operation_hash}.cache"),
        "w+",
        encoding="utf8",
    ) as f:
        CACHED_HASHES[current_operation_hash] = f.name
        for r in results:
            f.write(r + "\n")

        return f.name


def clear_cache():
    for filepath in glob.glob(os.path.join(CACHE_DIR, "*.cache")):
        try:
            os.remove(filepath)
        except:
            print(f"Cannot remove '{filepath}', skipping...")

    global CACHED_HASHES
    CACHED_HASHES = {}


populate_cached_hashes()
