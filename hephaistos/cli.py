from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser
from distutils import dir_util
import logging
from pathlib import Path
import sys
from typing import NoReturn

from hephaistos import backups, config, hashes, helpers, interactive, lua_mod, patchers, sjson_data
from hephaistos.config import LOGGER
from hephaistos.helpers import HadesNotFound, HUD, Scaling


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
        subparsers = self.add_subparsers(parser_class=ParserBase,
            help="one of:", metavar='subcommand', dest='subcommand')
        self.subcommands: dict[str, BaseSubcommand] = {
            'patch': PatchSubcommand(),
            'restore': RestoreSubcommand(),
            'status': StatusSubcommand(),
            'version': VersionSubcommand(),
        }
        for name, subcommand in self.subcommands.items():
            subparsers.add_parser(name, parents=[subcommand],
                description=subcommand.description, help=subcommand.description)
        self.__start()

    def __start(self):
        raw_args = sys.argv[1:]
        # if no argument is provided, enter interactive mode
        if len(raw_args) == 0:
            self.__interactive(raw_args)

        args = self.parse_args(raw_args)
        # handle global args
        self.__configure_logging(args.verbose)
        self.__configure_hades_dir(args.hades_dir)
        try:
            # handle subcommand args via SubcommandBase.dispatch handler
            args.dispatch(**vars(args))
        except Exception as e:
            LOGGER.exception(e) # log any unhandled exception
        # if in interactive mode, loop until user manually closes
        self.__restart() if config.interactive_mode else self.__end()

    def __interactive(self, raw_args: list[str]):
        config.interactive_mode = True
        interactive.clear()
        self.__configure_hades_dir('.')
        try:
            msg = f"""Hi! This interactive wizard will help you to set up Hephaistos.
Note: while Hephaistos can be used in interactive mode for basic usage, you will need to switch to non-interactive mode for any advanced usage. See the README for more details.

{helpers.check_version()}
"""
            print(msg)
            available_subcommands = {
                subcommand: helpers.capitalize(self.subcommands[subcommand].description)
                for subcommand in ['patch', 'restore', 'status']
            }
            subcommand = interactive.pick(
                add_option=interactive.EXIT_OPTION,
                **available_subcommands,
            )
            raw_args.append(subcommand)
            if subcommand == 'patch':
                choice = interactive.pick(
                    common219="Select from common 21:9 resolutions",
                    common329="Select from common 32:9 resolutions",
                    common489="Select from common 48:9 / triple screen resolutions",
                    manual="Input resolution manually",
                )
                if choice == 'common219':
                    (width, height) = interactive.pick(
                        prompt="Select resolution:",
                        options=[
                            '2560 x 1080',
                            '3440 x 1440',
                            '3840 x 1600',
                            '5120 x 2160',
                        ],
                    ).split(' x ')
                elif choice == 'common329':
                    (width, height) = interactive.pick(
                        prompt="Select resolution:",
                        options=[
                            '3840 x 1080',
                            '5120 x 1440',
                        ],
                    ).split(' x ')
                elif choice == 'common489':
                    (width, height) = interactive.pick(
                        prompt="Select resolution:",
                        options=[
                            '5760 x 1080',
                            '7680 x 1440',
                        ],
                    ).split(' x ')
                else:
                    width = interactive.input_number("Width: ")
                    height = interactive.input_number("Height: ")
                    print()
                raw_args.append(width)
                raw_args.append(height)
                choice = interactive.pick(
                    prompt="Select HUD preference (for 32:9, try out both options and see what you prefer!):",
                    expand="Expand HUD horizontally (recommended for 21:9)",
                    center="Keep HUD in the center (recommended for 48:9 / triple screen)",
                )
                raw_args.append('--hud')
                raw_args.append(choice)
            raw_args.append('-v') # auto-enable verbose mode
        except interactive.InteractiveCancel:
            self.__restart(prompt_user=False)
        except interactive.InteractiveExit:
            self.__end()

    def __configure_logging(self, verbose_arg: int):
        level = ParserBase.VERBOSE_TO_LOG_LEVEL[min(verbose_arg, 2)]
        LOGGER.setLevel(level)

    def __configure_hades_dir(self, hades_dir_arg: str):
        config.hades_dir = Path(hades_dir_arg)
        try:
            helpers.is_valid_hades_dir(config.hades_dir)
        except HadesNotFound as e:
            LOGGER.error(e)
            hades_dirs = helpers.try_detect_hades_dirs()
            if len(hades_dirs) > 0:
                advice = '\n'.join(f"  - {hades_dir}" for hades_dir in hades_dirs)
            else:
                advice = "  - Could not auto-detect any Hades directory."
            msg = f"""Hephaistos does not seem to be located in the Hades directory:
{advice}
Please move Hephaistos directly to the Hades directory.

If you know what you're doing, you can also re-run with '--hades-dir' to manually specify Hades directory while storing Hephaistos elsewhere."""
            LOGGER.error(msg)
            self.__end(1, prompt_user=config.interactive_mode)

    def __restart(self, prompt_user=True):
        if prompt_user:
            interactive.any_key("\nPress any key to continue...")
        interactive.clear()
        self.__start()

    def __end(self, exit_code=None, prompt_user=False):
        if prompt_user:
            interactive.any_key("\nPress any key to exit...")
        sys.exit(exit_code)


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
        super().__init__(description="patch Hades using Hephaistos", **kwargs)
        self.add_argument('width', type=int, help="display resolution width")
        self.add_argument('height', type=int, help="display resolution height")
        self.add_argument('--scaling', default=Scaling.HOR_PLUS,
            choices=[Scaling.HOR_PLUS.value, Scaling.PIXEL_BASED.value],
            help="scaling type (default: 'hor+')")
        self.add_argument('--hud', default=HUD.EXPAND,
            choices=[HUD.EXPAND.value, HUD.CENTER.value],
            help="HUD mode (default: 'expand')")
        self.add_argument('--no-custom-resolution', action='store_false',
            help="do not use custom resolution (default: use custom resolution, bypassing monitor resolution detection)")
        self.add_argument('-f', '--force', action='store_true',
            help="force patching, bypassing hash check and removing previous backups (useful after game update)")

    def handler(self, width: int, height: int, scaling: Scaling, hud: HUD, no_custom_resolution: bool, force: bool, **kwargs) -> None:
        """Compute viewport depending on arguments, then patch all needed files and install Lua mod.
        If using '--force', discard backups, hashes and SJSON data, and uninstall Lua mod."""
        helpers.configure_screen_variables(width, height, scaling)
        LOGGER.info(f"Using resolution: {config.resolution.width, config.resolution.height}")
        LOGGER.info(f"Using '--scaling={scaling}': computed patch viewport {config.new_screen.width, config.new_screen.height}")

        config.center_hud = True if hud == HUD.CENTER else False
        msg = f"Using '--hud={hud}': HUD will be kept in the center of the screen" if config.center_hud else f"Using '--hud={hud}': HUD will be expanded horizontally"
        LOGGER.info(msg)

        if no_custom_resolution == False:
            LOGGER.info("Using '--no-custom-resolution': will not bypass monitor resolution detection")
            config.custom_resolution = False

        if force:
            LOGGER.info("Using '--force': will discard all `hephaistos-data` and uninstall Lua mod prior to repatching")
            backups.discard()
            hashes.discard()
            sjson_data.discard()
            lua_mod.uninstall()

        try:
            patchers.patch_engines()
            patchers.patch_sjsons()
            lua_mod.install()
        except hashes.HashMismatch as e:
            LOGGER.error(e)
            if config.interactive_mode:
                LOGGER.error("It looks like the game was updated. Do you wish to discard previous backups and re-patch Hades from its current state?")
                choice = interactive.pick(options=['Yes', 'No',], add_option=None)
                if choice == 'Yes':
                    self.handler(width, height, scaling, hud, force=True)
            else:
                LOGGER.error("Was the game updated? Re-run with '--force' to discard previous backups and re-patch Hades from its current state.")
        except (LookupError, FileExistsError) as e:
            LOGGER.error(e)


class RestoreSubcommand(BaseSubcommand):
    def __init__(self, **kwargs) -> None:
        super().__init__(description="restore Hades to its pre-Hephaistos state", **kwargs)

    def handler(self, **kwargs) -> None:
        """Restore backups, discard hashes and SJSON data, uninstall Lua mod."""
        backups.restore()
        hashes.discard()
        sjson_data.discard()
        lua_mod.uninstall()
        # clean up Hephaistos data dir if empty (using standalone executable)
        if not any(config.HEPHAISTOS_DATA_DIR.iterdir()):
            dir_util.remove_tree(str(config.HEPHAISTOS_DATA_DIR))
            LOGGER.info(f"Cleaned up empty directory '{config.HEPHAISTOS_DATA_DIR}'")


class StatusSubcommand(BaseSubcommand):
    def __init__(self, **kwargs) -> None:
        super().__init__(description="check current Hades / Hephaistos status", **kwargs)

    def handler(self, **kwargs) -> None:
        """Check Hades and Hephaistos files and report back on probable current status."""
        hephaistos_data_checks = [
            backups.status(),
            hashes.status(),
            sjson_data.status(),
        ]
        hades_checks = [
            patchers.patch_engines_status(),
            lua_mod.status(),
        ]
        if all(hephaistos_data_checks) and all(hades_checks):
            print(f"Hades is correctly patched with Hephaistos.")
        elif all(hephaistos_data_checks):
            print(f"Hades was patched with Hephaistos, but Hades files were modified. Was the game updated?")
        elif all(hades_checks):
            print(f"Hades was patched with Hephaistos, but Hephaistos data files were lost. Was 'hephaistos-data' (or part of it) deleted?")
        else:
            print(f"Hades is not patched with Hephaistos.")


class VersionSubcommand(BaseSubcommand):
    def __init__(self, **kwargs) -> None:
        super().__init__(description="check Hephaistos version and if an update is available", **kwargs)

    def handler(self, **kwargs) -> None:
        """Check Hephaistos version and if an update is available."""
        print(helpers.check_version())
