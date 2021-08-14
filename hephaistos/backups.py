from distutils import dir_util, file_util
from pathlib import Path

from hephaistos import config
from hephaistos.config import LOGGER


BACKUP_DIR = config.HEPHAISTOS_DATA_DIR.joinpath('backups')


def get(file: Path) -> Path:
    backup_file = __get_file(file)
    if not backup_file.exists():
        raise LookupError(f"Backup file '{backup_file}' is missing")
    return backup_file


def store(file: Path) -> Path:
    backup_file = __get_file(file)
    if backup_file.exists():
        raise FileExistsError(f"Backup file '{backup_file}' already exists")
    backup_file.parent.mkdir(parents=True, exist_ok=True)
    file_util.copy_file(str(file), str(backup_file))
    LOGGER.debug(f"Backed up '{file}' to '{backup_file}'")
    return backup_file


def __get_file(file: Path) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    return BACKUP_DIR.joinpath(file)


def invalidate() -> None:
    if BACKUP_DIR.exists():
        dir_util.remove_tree(str(BACKUP_DIR))
    LOGGER.info(f"Invalidated backups at '{BACKUP_DIR}'")


def restore() -> None:
    if BACKUP_DIR.exists():
        dir_util.copy_tree(str(BACKUP_DIR), str(config.hades_dir))
        dir_util.remove_tree(str(BACKUP_DIR))
        LOGGER.info(f"Restored backups from '{BACKUP_DIR}' to '{config.hades_dir}'")
    else:
        LOGGER.info(f"No backups to restore from '{BACKUP_DIR}'")
