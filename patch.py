#!/usr/bin/env python3
"""Ultrawide patch

Patches engine DLL files to enable ultrawide resolution.
"""

import logging
from pathlib import Path
import re

# Logging
logging.basicConfig(level=logging.INFO)

# Files
DLL_FILES = {
    'DirectX': Path('x64/EngineWin64s.dll'),
    'Vulkan': Path('x64Vk/EngineWin64sv.dll'),
    '32-bit': Path('x86/EngineWin32s.dll'),
}
BACKUP_SUFFIX = '.bak'

# Byte patching fuckeries
BYTE_LENGTH = 4
BYTE_ORDER = 'little'
MOV_1920_REGEX = re.compile(b'(\xc7\x05.{4})' + (1920).to_bytes(BYTE_LENGTH, BYTE_ORDER))
MOV_1080_REGEX = re.compile(b'(\xc7\x05.{4})' + (1080).to_bytes(BYTE_LENGTH, BYTE_ORDER))


def get_backup(dll_file: Path) -> Path:
    return dll_file.with_suffix(dll_file.suffix + BACKUP_SUFFIX)


def patch(dll_file: Path, resolution_width: int) -> None:
    original_bytes = dll_file.read_bytes()

    backup_file = get_backup(dll_file)
    if not backup_file.exists():
        backup_file.write_bytes(original_bytes)
        logging.info("Backed up original {} to {}".format(dll_file, backup_file))

        patched_bytes = MOV_1920_REGEX.sub(b'\g<1>' + (resolution_width).to_bytes(BYTE_LENGTH, BYTE_ORDER), original_bytes)
        dll_file.write_bytes(patched_bytes)
        logging.info("Patched {} with resolution width {}".format(dll_file, resolution_width))
    else:
        logging.warning("Backup file already present -- cannot patch an already patched DLL, please restore original")


def restore(dll_file: Path) -> None:
    backup_file = get_backup(dll_file)
    if backup_file.exists():
        backup_file.replace(dll_file)
        logging.info("Restored {} from backup file".format(dll_file))
    else:
        logging.warning("Could not find backup file {}".format(backup_file))


if __name__ == '__main__':
    for backend, dll_file in DLL_FILES.items():
        logging.info("Patching {} backend...".format(backend))
        patch(dll_file, 2592)
        #restore(dll_file)
