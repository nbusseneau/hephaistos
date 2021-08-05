#!/usr/bin/env python3
"""Hephaistos

CLI tool for patching any resolution in Supergiant Games' Hades, initially
intended as an ultrawide support mod.
It can bypass both pillarboxing and letterboxing, which are the default on
non-16:9 resolutions for Hades.

See README for usage examples or run `hephaistos --help` for more information
about the available commands.
"""

from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser
from enum import Enum
import logging
from hashlib import sha256
from pathlib import Path
import re
import sys
from typing import NoReturn, Tuple

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


class SubcommandBase(ArgumentParser, metaclass=ABCMeta):
    def __init__(self, description: str, **kwargs):
        super().__init__(add_help=False, **kwargs)
        self.description = description
        self.set_defaults(dispatch=self.handler)

    @abstractmethod
    def handler(self, **kwargs) -> NoReturn:
        raise NotImplementedError("Subclasses must implement a handler method.")


class PatchCommand(SubcommandBase):
    """`patch` subcommand."""
    # Viewport
    DEFAULT_VIRTUAL_VIEWPORT = (1920, 1080)

    # Patching
    BYTE_LENGTH = 4
    BYTE_ORDER = 'little'
    MOV_1920_REGEX = re.compile(rb'(\xc7\x05.{4})' + (1920).to_bytes(BYTE_LENGTH, BYTE_ORDER))
    MOV_1080_REGEX = re.compile(rb'(\xc7\x05.{4})' + (1080).to_bytes(BYTE_LENGTH, BYTE_ORDER))
    EXPECTED_SUBS = 2

    def __init__(self, **kwargs):
        super().__init__(description="patch Hades binaries based on given display resolution", **kwargs)
        self.add_argument('width', type=int, help="display resolution width")
        self.add_argument('height', type=int, help="display resolution height")
        self.add_argument('-s', '--scaling', default=Scaling.HOR_PLUS,
            choices=[Scaling.HOR_PLUS.value, Scaling.PIXEL_BASED.value],
            help="scaling type (default: hor+)")
        self.add_argument('-f', '--force', action='store_true',
            help="force patching of current binaries, bypassing hash check and replacing previous backups (useful after game update)")
    
    def handler(self, width: int, height: int, scaling: Scaling, force: bool, **kwargs) -> None:
        """Compute viewport depending on arguments and iterate over DLL paths to patch it in."""
        patch_viewport = self.compute_viewport(width, height, scaling)
        logger.info(f"Computed patch viewport {patch_viewport} using scaling {scaling}")
        for engine, dll_filepath in DLL_FILEPATHS.items():
            logger.debug(f"Patching {engine} backend")
            self.patch(dll_filepath, patch_viewport, force)

    def compute_viewport(self, width: int, height: int, scaling: Scaling) -> Tuple[int, int]:
        """Compute virtual viewport size to patch depending on scaling type and display resolution width / height."""
        if scaling == Scaling.HOR_PLUS:
            (virtual_width, virtual_height) = PatchCommand.DEFAULT_VIRTUAL_VIEWPORT
            virtual_width = int(width / height * virtual_height)
            return (virtual_width, virtual_height)
        elif scaling == Scaling.PIXEL_BASED:
            return (width, height)
        else:
            raise ValueError("Unknown scaling type")

    def patch(self, dll_filepath: str, viewport: Tuple[int, int], force: bool) -> None:
        """Patch DLL at filepath with virtual width / height.

        On first run:
        - Store a backup copy of the original DLL for restoration with the `restore` subcommand.
        - Store patched hash in a JSON file (the "hash store").

        On subsequent runs, check current DLL hash against previously stored hash:
        - If matching, it is safe to repatch.
        - It not matching, the DLL has changed since the last patch: game was probably updated.
          Patching is stopped so that user may investigate.
        
        Providing `--force` bypasses the hash check and invalidates previous backups.
        """
        current_file = Path(dll_filepath)
        current_bytes = current_file.read_bytes()
        backup_file = BACKUP_DIR.joinpath(dll_filepath)
        hash_file = HASH_DIR.joinpath(dll_filepath).with_suffix(HASH_EXTENSION)

        # if using '--force', invalidate previous backup and stored hash
        if force and backup_file.exists():
            hash_file.unlink(missing_ok=True)
            backup_file.unlink()
            logger.info(f"Backup file {backup_file} invalidated due to '--force' usage")

        # otherwise, check current file hash against previously stored hash if exists
        elif hash_file.exists():
            current_hash = sha256(current_bytes).hexdigest()
            stored_hash = hash_file.read_text()
            logger.debug("Checking current DLL hash against previously stored hash")
            logger.debug(f"Current hash: {current_hash} | Stored hash: {stored_hash}")
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
            logger.debug(f"Backed up current {current_file} to {backup_file}")

        # patch and store hash for future reference
        (hex_width, hex_height) = [(value).to_bytes(PatchCommand.BYTE_LENGTH, PatchCommand.BYTE_ORDER) for value in viewport]
        (patched_bytes, width_sub_count) = PatchCommand.MOV_1920_REGEX.subn(b'\g<1>' + hex_width, current_bytes)
        (patched_bytes, height_sub_count) = PatchCommand.MOV_1080_REGEX.subn(b'\g<1>' + hex_height, patched_bytes)
        if width_sub_count == PatchCommand.EXPECTED_SUBS and height_sub_count == PatchCommand.EXPECTED_SUBS:
            patched_hash = sha256(patched_bytes).hexdigest()
            hash_file.parent.mkdir(parents=True, exist_ok=True)
            hash_file.write_text(patched_hash)
            logger.debug(f"Stored patched hash {patched_hash} in {hash_file}")
            current_file.write_bytes(patched_bytes)
            logger.info(f"Patched {current_file} with viewport {viewport}")
        else:
            logger.error(f"Expected {PatchCommand.EXPECTED_SUBS} matches, found {width_sub_count} for width and {height_sub_count} for height")


class RestoreCommand(SubcommandBase):
    """`restore` subcommand."""
    def __init__(self, **kwargs):
        super().__init__(description="restore Hades binaries from backed up originals", **kwargs)
    
    def handler(self, **kwargs) -> None:
        """Iterate over DLL paths and restore backups."""
        for engine, dll_filepath in DLL_FILEPATHS.items():
            logger.debug(f"Restoring {engine} backend")
            self.restore(dll_filepath)

    def restore(self, dll_filepath: str) -> None:
        """Restore DLL at filepath from backed up original. Also delete stored hash if any."""
        current_file = Path(dll_filepath)
        backup_file = BACKUP_DIR.joinpath(dll_filepath)
        # restore backup and delete stored hash if any
        if backup_file.exists():
            hash_file = HASH_DIR.joinpath(dll_filepath).with_suffix(HASH_EXTENSION)
            hash_file.unlink(missing_ok=True)
            backup_file.replace(current_file)
            logger.info(f"Restored {current_file} from backed up {backup_file}")
        else:
            logger.error(f"Could not find backup file {backup_file}")


class ParserBase(ArgumentParser):
    """Base parser for hosting shared behavior.

    - Print help when user supplies invalid arguments.
    - Shared arguments:
        - Verbosity level: `--verbose` (as repeatable `-v`)

    `ParserBase` serves as the base class for both the main CLI and the actual subcommand parsers.
    Counter-intuitively, the subcommands defined above MUST NOT directly inherit from `ParserBase`.
    This is due to how subparsers and parenting work in `argparse`:
    - When initializing subparsers via `add_subparsers`:
        - `parser_class` is provided as the base class to use for subcommand parsers.
    - When adding subparsers via `add_parser`:
        - A new instance of `parser_class` is instantiated.
        - If `parents` are provided, the parents' arguments are copied into the new instance.
        - This instance is the actual parser used for the subcommand.
    - Parents' types are ignored, and MUST NOT be the same as `parser_class` to avoid argument conflicts.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_argument('-v', '--verbose', action='count', default=0, help="verbosity level (none: default, '-v': info, '-vv': debug)")

    def error(self, message) -> NoReturn:
        """Print help when user supplies invalid arguments."""
        sys.stderr.write(f"error: {message}\n\n")
        self.print_help()
        sys.exit(2)


class Hephaistos(ParserBase):
    """Hephaistos entry point. Main parser for hosting the individual subcommands."""
    def __init__(self, **kwargs):
        super().__init__(description="Hephaistos CLI", **kwargs)
        subparsers = self.add_subparsers(parser_class=ParserBase, required=True, help="one of:", metavar='subcommand', dest='subcommand')
        subcommands = {
            'patch': PatchCommand(),
            'restore': RestoreCommand(),
        }
        for name, subcommand in subcommands.items():
            subparsers.add_parser(name, parents=[subcommand], description=subcommand.description, help=subcommand.description)

        # parse args and dispatch to subcommand via SubcommandBase.dispatch handler
        args = self.parse_args()
        if args.verbose:
            if args.verbose == 1:
                logger.setLevel(logging.INFO)
            if args.verbose >= 2:
                logger.setLevel(logging.DEBUG)
        args.dispatch(**vars(args))


if __name__ == '__main__':
    Hephaistos()
