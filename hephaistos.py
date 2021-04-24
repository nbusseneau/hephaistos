#!/usr/bin/env python3
"""Hephaistos

CLI tool able to patch virtual viewport in Hades engine DLL files with any given
resolution using Hor+ scaling (default) or pixel-based scaling.

Run `hephaistos.py --help` for more information about the available commands.
"""

from argparse import ArgumentParser
from enum import Enum
import logging
from hashlib import sha256
from pathlib import Path
import re
import sys
from typing import Tuple

# Logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger()


# Global variables
HEPHAISTOS_DIR = Path('hephaistos')
BACKUP_DIR = HEPHAISTOS_DIR.joinpath('backups')
HASH_DIR = HEPHAISTOS_DIR.joinpath('hashes')
HASH_EXTENSION = '.sha256'
DLL_FILEPATHS = {
    'DirectX': 'x64/EngineWin64s.dll',
    'Vulkan': 'x64Vk/EngineWin64sv.dll',
    '32-bit': 'x86/EngineWin32s.dll',
}


class Scaling(str, Enum):
    HOR_PLUS = 'hor+'
    PIXEL_BASED = 'pixel'


class PatchHandler:
    """Handler for the 'patch' subcommand."""
    # Viewport
    DEFAULT_VIRTUAL_VIEWPORT = (1920, 1080)

    # Patching
    BYTE_LENGTH = 4
    BYTE_ORDER = 'little'
    MOV_1920_REGEX = re.compile(b'(\xc7\x05.{4})' + (1920).to_bytes(BYTE_LENGTH, BYTE_ORDER))
    MOV_1080_REGEX = re.compile(b'(\xc7\x05.{4})' + (1080).to_bytes(BYTE_LENGTH, BYTE_ORDER))
    EXPECTED_SUBS = 2    
    
    def __init__(self, width: int, height: int, scaling: Scaling, force: bool, **kwargs):
        patch_viewport = self.compute_viewport(width, height, scaling)
        logger.info("Computed patch viewport {} using scaling {}".format(patch_viewport, scaling))
        for engine, dll_filepath in DLL_FILEPATHS.items():
            logger.debug("Patching {} backend".format(engine))
            self.patch(dll_filepath, patch_viewport, force)

    def compute_viewport(self, width: int, height: int, scaling: Scaling) -> Tuple[int, int]:
        """Compute virtual viewport size to patch depending on scaling type and resolution width / height."""
        if scaling == Scaling.HOR_PLUS:
            (virtual_width, virtual_height) = PatchHandler.DEFAULT_VIRTUAL_VIEWPORT
            virtual_width = int(width / height * virtual_height)
            return (virtual_width, virtual_height)
        elif scaling == Scaling.PIXEL_BASED:
            return (width, height)
        else:
            raise ValueError("Unknown scaling type")

    def patch(self, dll_filepath: str, viewport: Tuple[int, int], force: bool) -> None:
        """Patch DLL at filepath with virtual width / height.

        On first run:
        - Store a backup copy of the original DLL for restoration with the 'restore' subcommand.
        - Store patched hash in a JSON file (the "hash store").

        On subsequent runs, check current DLL hash against previously stored hash:
        - If matching, it is safe to repatch.
        - It not matching, the DLL has changed since the last patch: game was probably updated.
          Patching is stopped so that user may investigate.
        
        Providing '--force' bypasses the hash check and invalidates previous backups.
        """
        current_file = Path(dll_filepath)
        current_bytes = current_file.read_bytes()
        backup_file = BACKUP_DIR.joinpath(dll_filepath)
        hash_file = HASH_DIR.joinpath(dll_filepath).with_suffix(HASH_EXTENSION)

        # if using '--force', invalidate previous backup and stored hash
        if force and backup_file.exists():
            hash_file.unlink(missing_ok=True)
            backup_file.unlink()
            logger.info("Backup file {} invalidated due to '--force' usage".format(backup_file))

        # otherwise, check current file hash against previously stored hash if exists
        elif hash_file.exists():
            current_hash = sha256(current_bytes).hexdigest()
            stored_hash = hash_file.read_text()
            logger.debug("Checking current DLL hash against previously stored hash".format(current_hash, stored_hash))
            logger.debug("Current hash: {} | Stored hash: {}".format(current_hash, stored_hash))
            # if hashes match, we can repatch based on backup file
            if current_hash == stored_hash:
                current_bytes = backup_file.read_bytes()
            # otherwise, it is probable the game was updated
            else:
                msg = "Current file hash does not match previously stored hash -- was the game updated? If yes, re-run with '--force' to invalidate previous backups and re-patch."
                logger.error(msg)
                raise RuntimeError(msg)

        # create backup if none exists -- either on first run or following invalidation via '--force'
        if not backup_file.exists():
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            backup_file.write_bytes(current_bytes)
            logger.debug("Backed up current {} to {}".format(current_file, backup_file))

        # patch and store hash for future reference
        (hex_width, hex_height) = [(value).to_bytes(PatchHandler.BYTE_LENGTH, PatchHandler.BYTE_ORDER) for value in viewport]
        (patched_bytes, width_sub_count) = PatchHandler.MOV_1920_REGEX.subn(b'\g<1>' + hex_width, current_bytes)
        (patched_bytes, height_sub_count) = PatchHandler.MOV_1080_REGEX.subn(b'\g<1>' + hex_height, patched_bytes)
        if width_sub_count == PatchHandler.EXPECTED_SUBS and height_sub_count == PatchHandler.EXPECTED_SUBS:
            patched_hash = sha256(patched_bytes).hexdigest()
            hash_file.parent.mkdir(parents=True, exist_ok=True)
            hash_file.write_text(patched_hash)
            logger.debug("Stored patched hash {} in {}".format(patched_hash, hash_file))
            current_file.write_bytes(patched_bytes)
            logger.info("Patched {} with viewport {}".format(current_file, viewport))
        else:
            logger.error("Expected {} matches, found {} for width and {} for height".format(PatchHandler.EXPECTED_SUBS, width_sub_count, height_sub_count))


class RestoreHandler:
    """Handler for the 'restore' subcommand."""
    def __init__(self, **kwargs):
        for engine, dll_filepath in DLL_FILEPATHS.items():
            logger.debug("Restoring {} backend".format(engine))
            self.restore(dll_filepath)

    def restore(self, dll_filepath: str) -> None:
        """Restore DLL at filepath from backed up original."""
        current_file = Path(dll_filepath)
        backup_file = BACKUP_DIR.joinpath(dll_filepath)
        # restore backup and invalidate stored hash if any
        if backup_file.exists():
            hash_file = HASH_DIR.joinpath(dll_filepath).with_suffix(HASH_EXTENSION)
            hash_file.unlink(missing_ok=True)
            backup_file.replace(current_file)
            logger.info("Restored {} from backed up {}".format(current_file, backup_file))
        else:
            logger.error("Could not find backup file {}".format(backup_file))


class PrintHelpOnErrorParser(ArgumentParser):
    """Simple parser printing help when user supplies invalid arguments, rather than leaving them hanging."""
    def error(self, message):
        sys.stderr.write("error: {}\n\n".format(message))
        self.print_help()
        sys.exit(2)


if __name__ == '__main__':
    # Command line interface
    parser = PrintHelpOnErrorParser(description="Hephaistos CLI")
    shared_args = PrintHelpOnErrorParser(add_help=False)
    shared_args.add_argument('-v', '--verbose', action='count', default=0, help="verbosity level (none: default, '-v': info, '-vv': debug)")
    subparsers = parser.add_subparsers(required=True, help="one of:", metavar='subcommand', dest='subcommand')
    
    # Patch subcommand
    patch_description = "patch a specific screen resolution in Hades binaries"
    patch_subcommand = subparsers.add_parser('patch', description=patch_description, parents=[shared_args], help=patch_description)
    patch_subcommand.add_argument('width', type=int, help="screen width")
    patch_subcommand.add_argument('height', type=int, help="screen height")
    patch_subcommand.add_argument('-s', '--scaling', default=Scaling.HOR_PLUS,
        choices=[Scaling.HOR_PLUS.value, Scaling.PIXEL_BASED.value],
        help="scaling type (default: hor+)")
    patch_subcommand.add_argument('-f', '--force', action='store_true',
        help="force patching of current binaries, bypassing hash check and replacing previous backups (useful after game update)")
    patch_subcommand.set_defaults(handler=PatchHandler)
    
    # Restore subcommand
    restore_description = "restore Hades binaries from backed up originals"
    restore_subcommand = subparsers.add_parser('restore', description=restore_description, parents=[shared_args], help=restore_description)
    restore_subcommand.set_defaults(handler=RestoreHandler)
    
    # Parse args, set log level, and execute
    args = parser.parse_args()
    if args.verbose:
        if args.verbose == 1:
            logger.setLevel(logging.INFO)
        if args.verbose >= 2:
            logger.setLevel(logging.DEBUG)
    args.handler(**vars(args))
