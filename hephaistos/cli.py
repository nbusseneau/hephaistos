from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser
import logging
import sys
from typing import NoReturn

from hephaistos import backups, config, hashes, helpers, lua_mod, patchers
from hephaistos import helpers
from hephaistos.config import LOGGER
from hephaistos.helpers import Scaling


class ParserBase(ArgumentParser):
    """Base parser for hosting shared behavior.

    - Print help when user supplies invalid arguments.
    - Shared arguments (verbosity, etc.).

    `ParserBase` serves as the base class for both the main CLI and the actual subcommand parsers,
    even if not defined as such (`BaseSubcommand` and children inherit from `ArgumentParser`).
    
    Counter-intuitively, the defined subcommand parsers must NOT directly inherit from `ParserBase`.
    This is due to how subparsers and parenting work in `argparse`:
    - When initializing subparsers via `add_subparsers`:
        - `parser_class` is provided as the base class to use for subcommand parsers.
    - When adding subparsers via `add_parser`:
        - A new instance of `parser_class` is instantiated.
        - If `parents` are provided, the parents' arguments are copied into the `parser_class` instance.
        - This new `parser_class` instance is the actual parser used for the subcommand.
    
    This means the actual type of the subparser is ignored, and must NOT be the same as
    `parser_class` to avoid argument conflicts while copying. This explains why only the main
    Hephaistos CLI is declared as deriving from `ParserBase`, even though at runtime all parsers
    (including `BaseSubcommand`) will inherit from `ParserBase`.
    """
    VERBOSE_TO_LOG_LEVEL = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.add_argument('-v', '--verbose', action='count', default=0,
            help="verbosity level (none: errors only, '-v': info, '-vv': debug)")
        self.add_argument('--hades-dir', default='.',
            help="path to Hades directory (default: '.', i.e. current directory)")

    def error(self, message) -> NoReturn:
        """Print help when user supplies invalid arguments."""
        sys.stderr.write(f"error: {message}\n\n")
        self.print_help()
        sys.exit(2)


class Hephaistos(ParserBase):
    """Hephaistos entry point. Main parser for hosting the individual subcommands."""
    def __init__(self, **kwargs) -> None:
        super().__init__(prog=config.HEPHAISTOS_NAME, description="Hephaistos CLI", **kwargs)
        subparsers = self.add_subparsers(parser_class=ParserBase, required=True,
            help="one of:", metavar='subcommand', dest='subcommand')
        subcommands = {
            'patch': PatchSubcommand(),
            'restore': RestoreSubcommand(),
        }
        for name, subcommand in subcommands.items():
            subparsers.add_parser(name, parents=[subcommand],
                description=subcommand.description, help=subcommand.description)
        args = self.parse_args()

        # handle global args
        self.__configure_logging(args.verbose)
        config.hades_dir = helpers.get_hades_dir(args.hades_dir)

        # handle subcommand args via SubcommandBase.dispatch handler
        try:
            args.dispatch(**vars(args))
        except Exception as e:
            LOGGER.exception(e) # log any unhandled exception

    def __configure_logging(self, verbosity: int):
        level = ParserBase.VERBOSE_TO_LOG_LEVEL[min(verbosity, 2)]
        LOGGER.setLevel(level)


class BaseSubcommand(ArgumentParser, metaclass=ABCMeta):
    def __init__(self, description: str, **kwargs) -> None:
        super().__init__(add_help=False, **kwargs)
        self.description = description
        self.set_defaults(dispatch=self.handler)

    @abstractmethod
    def handler(self, **kwargs) -> None:
        raise NotImplementedError("Subclasses must implement a handler method.")


class PatchSubcommand(BaseSubcommand):
    def __init__(self, **kwargs) -> None:
        super().__init__(description="patch Hades based on given display resolution", **kwargs)
        self.add_argument('width', type=int, help="display resolution width")
        self.add_argument('height', type=int, help="display resolution height")
        self.add_argument('-s', '--scaling', default=Scaling.HOR_PLUS,
            choices=[Scaling.HOR_PLUS.value, Scaling.PIXEL_BASED.value],
            help="scaling type (default: hor+)")
        self.add_argument('-f', '--force', action='store_true',
            help="force patching, bypassing hash check and removing previous backups (useful after game update)")

    def handler(self, width: int, height: int, scaling: Scaling, force: bool, **kwargs) -> None:
        """Compute viewport depending on arguments, then patch all needed files and install Lua mod.
        If using '--force', invalidate backups and hashes."""
        config.new_viewport = helpers.compute_viewport(width, height, scaling)
        LOGGER.info(f"Computed patch viewport {config.new_viewport} using scaling {scaling}")

        if force:
            backups.invalidate()
            hashes.invalidate()

        try:
            patchers.patch_engines()
            patchers.patch_sjsons()
            lua_mod.install()
        except hashes.HashMismatch as e:
            LOGGER.error(e)
            LOGGER.error("Was the game updated? Re-run with '--force' to invalidate previous backups and re-patch Hades from its current state.")
        except (LookupError, FileExistsError) as e:
            LOGGER.error(e)


class RestoreSubcommand(BaseSubcommand):
    def __init__(self, **kwargs) -> None:
        super().__init__(description="restore Hades to its pre-Hephaistos state", **kwargs)

    def handler(self, **kwargs) -> None:
        """Restore all backups, invalidate all hashes, uninstall Lua mod."""
        backups.restore()
        hashes.invalidate()
        lua_mod.uninstall()
