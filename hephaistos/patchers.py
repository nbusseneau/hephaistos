from collections import OrderedDict
from copy import deepcopy
from functools import singledispatch
import logging
import os.path
from pathlib import Path
import re
from typing import Callable, Pattern, Tuple

import sjson

from hephaistos import backups, config, hashes, helpers
from hephaistos.helpers import IntOrFloat, SJSON


logger = logging.getLogger(__name__)


def __safe_patch_file(file: Path, callback: Callable[..., None], *args, **kwargs) -> None:
    """Patch file using the given callback method in a safe manner, wrapped by
    backup and hash handling.

    On first run:
    - Store a backup copy of the original file for restoration with the `restore` subcommand.
    - Store patched hash in a text file.

    On subsequent runs, check current hash against previously stored hash:
    - If matching, it is safe to repatch from the backup copy.
    - It not matching, the file has changed since the last patch.
    """
    if hashes.check(file):
        logger.debug(f"Hash match for '{file}' -- repatching based on backup file")
        original_file = backups.get(file)
    else:
        logger.debug(f"No hash stored for '{file}' -- storing backup file")
        original_file = backups.store(file)
    callback(original_file, file, *args, **kwargs)
    hashes.store(file)


ENGINES = {
    'DirectX': 'x64/EngineWin64s.dll',
    'Vulkan': 'x64Vk/EngineWin64sv.dll',
    '32-bit': 'x86/EngineWin32s.dll',
}
BYTE_LENGTH = 4
BYTE_ORDER = 'little'
EXPECTED_SUBS = 2


def patch_engines() -> None:
    (current_width, current_height) = config.DEFAULT_VIRTUAL_VIEWPORT
    width_regex = re.compile(rb'(\xc7\x05.{4})' + __int_to_bytes(current_width))
    height_regex = re.compile(rb'(\xc7\x05.{4})' + __int_to_bytes(current_height))
    regexes = (width_regex, height_regex)

    for engine, filepath in ENGINES.items():
        file = config.hades_dir.joinpath(filepath)
        logger.debug(f"Patching {engine} backend at '{file}'")
        __safe_patch_file(file, __patch_engine, regexes)


def __int_to_bytes(value: int) -> bytes:
    return value.to_bytes(BYTE_LENGTH, BYTE_ORDER)


def __patch_engine(original_file: Path, file: Path, regexes: Tuple[Pattern[bytes], Pattern[bytes]]
) -> None:
    source_bytes = original_file.read_bytes()
    (hex_width, hex_height) = [__int_to_bytes(value) for value in config.new_viewport]
    (patched_bytes, width_sub_count) = regexes[0].subn(b'\g<1>' + hex_width, source_bytes)
    (patched_bytes, height_sub_count) = regexes[1].subn(b'\g<1>' + hex_height, patched_bytes)

    if width_sub_count != EXPECTED_SUBS or height_sub_count != EXPECTED_SUBS:
        msg = f"Expected {EXPECTED_SUBS} matches, found {width_sub_count} for width and {height_sub_count} for height"
        logger.error(msg)
        raise LookupError(msg)
    file.write_bytes(patched_bytes)
    logger.info(f"Patched '{file}' with viewport {config.new_viewport}")


SJSON_DIR = 'Content/Game/GUI'


def patch_sjsons() -> None:
    sjson_dir = config.hades_dir.joinpath(SJSON_DIR)
    for file in sjson_dir.glob('*.sjson'):
        logger.debug(f"Patching SJSON file at '{file}'")
        __safe_patch_file(file, __patch_sjson_file)


def __patch_sjson_file(original_file: Path, file: Path) -> None:
    source_sjson = sjson.loads(original_file.read_text())
    patched_sjson = __patch_sjson_data(source_sjson)
    file.write_text(sjson.dumps(patched_sjson))
    logger.info(f"Patched '{file}' with viewport {config.new_viewport}")


@singledispatch
def __patch_sjson_data(data: OrderedDict, previous_path: str=None) -> SJSON:
    patched = deepcopy(data)
    for key, value in data.items():
        current_path = key if previous_path is None else f'{previous_path}.{key}'
        patched[key] = __patch_sjson_data(value, current_path)
    return patched


@__patch_sjson_data.register
def _(data: list, previous_path: str=None) -> SJSON:
    patched = deepcopy(data)
    current_path = '[]' if previous_path is None else f'{previous_path}.[]'
    return [__patch_sjson_data(item, current_path) for item in patched]


@__patch_sjson_data.register
def _(data: str, previous_path: str=None) -> SJSON:
    try:
        numeric_value = float(data) if '.' in data else int(data)
        return __patch_sjson_data(numeric_value, previous_path)
    except ValueError:
        return data


@__patch_sjson_data.register(int)
@__patch_sjson_data.register(float)
def _(data: IntOrFloat, previous_path: str=None) -> SJSON:
    (width, height) = config.new_viewport
    key = previous_path.split('.')[-1]
    if key in ['X', 'MinX', 'MaxX', 'Width', 'FreeFormSelectMaxGridDistance']:
        patched = helpers.recompute_fixed_X(data, width)
        logger.debug(f"Patched '{previous_path}' from {data} to {patched}")
        return patched
    elif key in ['Y', 'MinY', 'MaxY', 'Height']:
        patched = helpers.recompute_fixed_Y(data, height)
        logger.debug(f"Patched '{previous_path}' from {data} to {patched}")
        return patched
    else:
        return data


HOOK_FILE = 'Content/Scripts/RoomManager.lua'
IMPORT_COMMAND = 'Import "{0}"'


def patch_lua(mod_entry_point: Path) -> None:
    hook_file = config.hades_dir.joinpath(HOOK_FILE)
    logger.debug(f"Patching Lua hook file at '{hook_file}'")
    __safe_patch_file(hook_file, __patch_hook_file, mod_entry_point)


def __patch_hook_file(original_file: Path, file: Path, mod_entry_point: Path) -> None:
    import_relative_path = os.path.relpath(mod_entry_point, file.parent)
    # replace backward slashes with forward slashes on Windows
    import_relative_path = import_relative_path.replace('\\', '/')
    statement = IMPORT_COMMAND.format(import_relative_path)
    source_text = original_file.read_text()
    source_text += f"""
-- Hephaistos hook
{statement}
"""
    file.write_text(source_text)
    logger.info(f"Patched '{file}' with hook '{statement}'")
