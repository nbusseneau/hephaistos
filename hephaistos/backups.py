from distutils import dir_util, file_util
import logging
from pathlib import Path

from hephaistos import config


logger = logging.getLogger(__name__)
BACKUP_DIR = config.HEPHAISTOS_DIR.joinpath('backups')


def get(file: Path) -> Path:
    backup_file = __get_file(file)
    if not backup_file.exists():
        msg = f"Backup file '{backup_file}' is missing"
        logger.error(msg)
        raise LookupError(msg)
    return backup_file


def store(file: Path) -> Path:
    backup_file = __get_file(file)
    if backup_file.exists():
        msg = f"Backup file '{backup_file}' already exists"
        logger.error(msg)
        raise FileExistsError(msg)
    backup_file.parent.mkdir(parents=True, exist_ok=True)
    file_util.copy_file(str(file), str(backup_file))
    logger.debug(f"Backed up '{file}' to '{backup_file}'")
    return backup_file


def __get_file(file: Path) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    return BACKUP_DIR.joinpath(file)


def invalidate() -> None:
    if BACKUP_DIR.exists():
        dir_util.remove_tree(str(BACKUP_DIR))
    logger.info(f"Invalidated backups at '{BACKUP_DIR}'")


def restore() -> None:
    if BACKUP_DIR.exists():
        dir_util.copy_tree(str(BACKUP_DIR), str(config.hades_dir))
        dir_util.remove_tree(str(BACKUP_DIR))
    logger.info(f"Restored backups from '{BACKUP_DIR}' to '{config.hades_dir}'")
