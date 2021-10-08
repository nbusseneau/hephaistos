from distutils import dir_util, file_util
from pathlib import Path

from hephaistos import config
from hephaistos.config import LOGGER


def get(file: Path) -> Path:
    backup_file = __get_file(file)
    if not backup_file.exists():
        raise LookupError(f"Backup file '{backup_file}' is missing")
    return backup_file


def store(file: Path) -> Path:
    backup_file = __get_file(file)
    if backup_file.exists() and not config.force:
        raise FileExistsError(f"Backup file '{backup_file}' already exists")
    backup_file.parent.mkdir(parents=True, exist_ok=True)
    file_util.copy_file(str(file), str(backup_file))
    LOGGER.debug(f"Backed up '{file}' to '{backup_file}'")
    return backup_file


def __get_file(file: Path) -> Path:
    config.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    return config.BACKUP_DIR.joinpath(file)


def restore() -> None:
    if config.BACKUP_DIR.exists():
        dir_util.copy_tree(str(config.BACKUP_DIR), str(config.hades_dir))
        dir_util.remove_tree(str(config.BACKUP_DIR))
        LOGGER.info(f"Restored backups from '{config.BACKUP_DIR}' to '{config.hades_dir}'")
    else:
        LOGGER.info(f"No backups to restore from '{config.BACKUP_DIR}'")


def status() -> None:
    if config.BACKUP_DIR.exists():
        LOGGER.info(f"Found backups at '{config.BACKUP_DIR}'")
        return True
    else:
        LOGGER.info(f"No backups found at '{config.BACKUP_DIR}'")
        return False
