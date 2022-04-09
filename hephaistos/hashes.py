from distutils import dir_util
import hashlib
from pathlib import Path

from hephaistos import config
from hephaistos.config import LOGGER


HASH_FILE_EXTENSION = '.sha256'


def check(file: Path) -> None:
    hash_file = __get_file(file)
    if not hash_file.exists():
        return False
    stored_hash = hash_file.read_text()
    current_hash = hashlib.sha256(file.read_bytes()).hexdigest()
    if current_hash != stored_hash:
        raise HashMismatch(f"Hash file mismatch: '{file}' was modified.")
    return True


def store(file: Path) -> Path:
    hash_file = __get_file(file)
    hash_file.parent.mkdir(parents=True, exist_ok=True)
    hash_file.write_text(hashlib.sha256(file.read_bytes()).hexdigest())
    LOGGER.debug(f"Stored hash for '{file}' at '{hash_file}'")
    return hash_file


def __get_file(file: Path) -> Path:
    config.HASH_DIR.mkdir(parents=True, exist_ok=True)
    return config.HASH_DIR.joinpath(file.relative_to(config.hades_dir)).with_suffix(HASH_FILE_EXTENSION)


def discard() -> None:
    if config.HASH_DIR.exists():
        dir_util.remove_tree(str(config.HASH_DIR))
        LOGGER.info(f"Discarded hashes at '{config.HASH_DIR}'")


def status() -> None:
    if config.HASH_DIR.exists() and any(config.HASH_DIR.iterdir()):
        LOGGER.info(f"Found hashes at '{config.HASH_DIR}'")
        return True
    else:
        LOGGER.info(f"No hashes found at '{config.HASH_DIR}'")
        return False


class HashMismatch(LookupError): ...
