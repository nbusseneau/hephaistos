from distutils import dir_util
import json
from pathlib import Path

import sjson

from hephaistos import config
from hephaistos.config import LOGGER


SJSON_DATA_DIR = config.HEPHAISTOS_DATA_DIR.joinpath('sjson_data')


def get(file: Path) -> Path:
    sjson_data_file = __get_file(file)
    if not sjson_data_file.exists():
        raise LookupError(f"SJSON data file '{sjson_data_file}' is missing")
    return json.loads(sjson_data_file.read_bytes())


def store(file: Path) -> Path:
    sjson_data_file = __get_file(file)
    if sjson_data_file.exists():
        raise FileExistsError(f"SJSON data file '{sjson_data_file}' already exists")
    data = sjson.loads(file.read_text())
    sjson_data_file.parent.mkdir(parents=True, exist_ok=True)
    sjson_data_file.write_text(json.dumps(data))
    LOGGER.debug(f"Saved SJSON data from '{file}' to '{sjson_data_file}'")
    return data


def __get_file(file: Path) -> Path:
    SJSON_DATA_DIR.mkdir(parents=True, exist_ok=True)
    return SJSON_DATA_DIR.joinpath(file)


def discard() -> None:
    if SJSON_DATA_DIR.exists():
        dir_util.remove_tree(str(SJSON_DATA_DIR))
    LOGGER.info(f"Discarded SJSON data at '{SJSON_DATA_DIR}'")
