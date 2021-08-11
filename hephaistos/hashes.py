from distutils import dir_util
import hashlib
import logging
from pathlib import Path

from hephaistos import config


logger = logging.getLogger(__name__)
HASH_DIR = config.HEPHAISTOS_DIR.joinpath('hashes')
HASH_FILE_EXTENSION = '.sha256'


def check(file: Path) -> None:
    hash_file = __get_file(file)
    if not hash_file.exists():
        return False
    stored_hash = hash_file.read_text()
    current_hash = hashlib.sha256(file.read_bytes()).hexdigest()
    if current_hash != stored_hash:
        msg = f"Stored hash for '{file}' does not match the current file -- it was modified."
        logger.error(msg)
        raise LookupError(msg)
    return True


def store(file: Path) -> Path:
    hash_file = __get_file(file)
    hash_file.parent.mkdir(parents=True, exist_ok=True)
    hash_file.write_text(hashlib.sha256(file.read_bytes()).hexdigest())
    logger.debug(f"Stored hash for '{file}' at '{hash_file}'")
    return hash_file


def __get_file(file: Path) -> Path:
    HASH_DIR.mkdir(parents=True, exist_ok=True)
    return HASH_DIR.joinpath(file).with_suffix(HASH_FILE_EXTENSION)


def invalidate() -> None:
    if HASH_DIR.exists():
        dir_util.remove_tree(str(HASH_DIR))
    logger.info(f"Invalidated hashes at '{HASH_DIR}'")
