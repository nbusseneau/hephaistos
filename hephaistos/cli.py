from abc import ABCMeta, abstractmethod
from argparse import ArgumentParser
from distutils import dir_util
import logging
from pathlib import Path
import sys
from typing import NoReturn

from hephaistos import backups, config, hashes, helpers, interactive, lua_mod, patchers, sjson_data
from hephaistos.config import LOGGER
from hephaistos.helpers import AspectRatio, HadesNotFound, HUD, ModImporterRuntimeError, Platform, Scaling


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
        self.add_argument('--no-modimporter', action='store_false', default=True, dest='modimporter',
            help="do not use modimporter for registering / unregistering Hephaistos (default: use modimporter if available)")

    def error(self, message) -> NoReturn:
        """Print help when user supplies invalid arguments."""
        sys.stderr.write(f"error: {message}\n\n")
        self.print_help()
        sys.exit(2)


CONTENT_DIR_PATH = {
    Platform.WINDOWS: 'Content',
    Platform.MS_STORE: 'Content/Content',
    Platform.MACOS: 'Game.macOS.app/Contents/Resources/Content',
    Platform.LINUX: 'Content',
}


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

    def __start(self) -> None:
        raw_args = sys.argv[1:]
        args = self.parse_args(raw_args)
        # if subcommand is provided, do not use interactive mode
        if args.subcommand:
            config.interactive_mode = False
        # handle global args early
        self.__handle_global_args(args)
        # if using interactive mode, launch it to set up subcommand and args
        if config.interactive_mode:
            # if verbosity not set by user, default to INFO logs in interactive
            if not args.verbose:
                LOGGER.setLevel(logging.INFO)
            args = self.__interactive(raw_args)
        # handle subcommand args via SubcommandBase.dispatch handler
        try:
            args.dispatch(**vars(args))
        except ModImporterRuntimeError as e:
            LOGGER.error(e)
        except Exception as e:
            LOGGER.exception(e) # log any unhandled exception
        # if in interactive mode, loop until user manually closes
        self.__restart() if config.interactive_mode else self.__end()

    def __handle_global_args(self, args: list[str]) -> None:
        # logging verbosity level
        level = ParserBase.VERBOSE_TO_LOG_LEVEL[min(args.verbose, 2)]
        LOGGER.setLevel(level)
        # hades_dir
        self.__configure_hades_dir(args.hades_dir)
        # modimporter
        if args.modimporter:
            config.modimporter = helpers.try_get_modimporter()
        else:
            LOGGER.info("Using '--no-modimporter': will not run 'modimporter', even if available")

    def __configure_hades_dir(self, hades_dir_arg: str) -> None:
        # if we are on macOS and running PyInstaller executable and defaulting
        # to current directory, force working directory to be the one containing
        # the executable
        # this is a kludge around macOS calling executables from the user home
        # rather than the current directory when double-clicked on from Finder
        if config.platform == Platform.MACOS and getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS') and hades_dir_arg == '.':
            hades_dir_arg = Path(sys.argv[0]).parent
            LOGGER.debug(f"Running macOS executable from Finder: forced working directory to {hades_dir_arg}")
        config.hades_dir = Path(hades_dir_arg)
        try:
            helpers.is_valid_hades_dir(config.hades_dir)
            config.content_dir = config.hades_dir.joinpath(CONTENT_DIR_PATH[config.platform])
            LOGGER.debug(f"Detected platform: {config.platform}")
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

    def __interactive(self, raw_args: list[str]) -> None:
        interactive.clear()
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
                options=available_subcommands,
                additional_option=interactive.EXIT_OPTION,
            )
            raw_args.append(subcommand)
            if subcommand == 'patch':
                self.__interactive_patch_handler(raw_args)
            # repass modified raw_args to parse_args after selection is done
            return self.parse_args(raw_args)
        except interactive.InteractiveCancel:
            self.__restart(prompt_user=False)
        except interactive.InteractiveExit:
            self.__end()

    def __interactive_patch_handler(self, raw_args) -> None:
        options = {
            AspectRatio._16_10: "Select from common 16:10 resolutions",
            AspectRatio._21_9: "Select from common 21:9 resolutions",
            AspectRatio._32_9: "Select from common 32:9 resolutions",
            AspectRatio._48_9: "Select from common 48:9 resolutions",
            AspectRatio.manual: "Input resolution manually",
        }
        aspect_ratio = interactive.pick(options=options)
        dispatch = {
            AspectRatio._16_10: lambda: self.__interactive_pick_resolution([
                '1280 x 800',
                '1440 x 900',
                '1680 x 1050',
                '1920 x 1200',
                '2560 x 1600',
                '3840 x 2400',
            ]),
            AspectRatio._21_9: lambda: self.__interactive_pick_resolution([
                '2560 x 1080',
                '3440 x 1440',
                '3840 x 1600',
                '5120 x 2160',
            ]),
            AspectRatio._32_9: lambda: self.__interactive_pick_resolution([
                '3840 x 1080',
                '5120 x 1440',
            ]),
            AspectRatio._48_9: lambda: self.__interactive_pick_resolution([
                '5760 x 1080',
                '7680 x 1440',
            ]),
            AspectRatio.manual: self.__interactive_input_resolution,
        }
        (width, height) = dispatch[aspect_ratio]()
        raw_args += [width, height]

        enabled = "enabled"
        recommended = "recommended"
        args = {
            AspectRatio._16_10: {
                enabled: [Scaling.VERT_PLUS, Scaling.PIXEL_BASED],
                recommended: Scaling.VERT_PLUS
            },
            AspectRatio._21_9: {
                enabled: [Scaling.HOR_PLUS, Scaling.PIXEL_BASED],
                recommended: Scaling.HOR_PLUS
            },
            AspectRatio._32_9: {
                enabled: [Scaling.HOR_PLUS, Scaling.PIXEL_BASED],
                recommended: Scaling.HOR_PLUS
            },
            AspectRatio._48_9: {
                enabled: [Scaling.HOR_PLUS, Scaling.PIXEL_BASED],
                recommended: Scaling.HOR_PLUS
            },
            AspectRatio.manual: {
                enabled: [Scaling.AUTODETECT, Scaling.PIXEL_BASED],
                recommended: Scaling.AUTODETECT
            },
        }
        scaling = self.__interactive_pick_scaling(enabled=args[aspect_ratio][enabled], recommended=args[aspect_ratio][recommended])
        # this is a kludge to allow manual selection of `Scaling.AUTODETECT`
        # we can't pass `Scaling.AUTODETECT`` to `--scaling` because it's not
        # one of the values allowed by `argparse.choices`, however, since
        # `Scaling.AUTODETECT` is the `argparse.default` value, not passing
        # anything does what we want
        if scaling != Scaling.AUTODETECT:
            raw_args += ['--scaling', scaling]

        recommended = {
            AspectRatio._16_10: HUD.EXPAND,
            AspectRatio._21_9: HUD.EXPAND,
            AspectRatio._32_9: None,
            AspectRatio._48_9: HUD.CENTER,
            AspectRatio.manual: None,
        }
        hud = self.__interactive_pick_hud(recommended=recommended[aspect_ratio])
        raw_args += ['--hud', hud]

        return raw_args

    def __interactive_pick_resolution(self, options: list[str]) -> tuple[int, int]:
        return interactive.pick(prompt="Select resolution:", options=options).split(' x ')

    def __interactive_input_resolution(self) -> tuple[int, int]:
        width = interactive.input_number("Width: ")
        height = interactive.input_number("Height: ")
        print()
        return (width, height)

    def __interactive_pick_scaling(self, enabled: list[Scaling], recommended: Scaling=None):
        options = {
            Scaling.AUTODETECT: "Hor+ / Vert+ (based on input resolution): keeps experience close to vanilla game.",
            Scaling.HOR_PLUS: "Hor+: keeps experience close to vanilla game.",
            Scaling.VERT_PLUS: "Vert+: keeps experience close to vanilla game.",
            Scaling.PIXEL_BASED: """Pixel-based: effectively "zooms out" the camera.""",
        }
        options = {option: description for option, description in options.items() if option in enabled}
        return interactive.pick(prompt="Select scaling algorithm (see README for more details):", options=options, recommended_option=recommended)

    def __interactive_pick_hud(self, recommended: HUD=None) -> HUD:
        options = {
            HUD.EXPAND: "Expand the HUD horizontally and vertically.",
            HUD.CENTER: "Keep HUD in the center of the screen with the same size as the original 16:9 HUD.",
        }
        return interactive.pick(prompt="Select HUD resizing mode (see README for more details):", options=options, recommended_option=recommended)

    def __restart(self, prompt_user=True) -> None:
        if prompt_user:
            interactive.any_key("\nPress any key to continue...")
        interactive.clear()
        self.__start()

    def __end(self, exit_code=None, prompt_user=False) -> None:
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
        self.add_argument('--scaling', type=Scaling, default=Scaling.AUTODETECT,
            choices=[Scaling.HOR_PLUS.value, Scaling.VERT_PLUS.value, Scaling.PIXEL_BASED.value],
            help="scaling algorithm (default: 'hor+' for wider aspect ratios / 'vert+' for taller aspect ratios)")
        self.add_argument('--hud', type=HUD, default=HUD.AUTODETECT,
            choices=[HUD.EXPAND.value, HUD.CENTER.value],
            help="HUD mode (default: 'expand' for most aspect ratios / 'center' for 48:9 and wider)")
        self.add_argument('--no-custom-resolution', action='store_false', default=True, dest='custom_resolution',
            help="do not patch custom resolution in 'ProfileX.sjson' configuration file (default: patch custom resolution)")
        self.add_argument('-f', '--force', action='store_true',
            help="force patching, bypassing hash check and removing previous backups (to be used after a game update)")

    def handler(self, width: int, height: int, scaling: Scaling, hud: HUD, custom_resolution: bool, force: bool, **kwargs) -> None:
        """Compute viewport depending on arguments, then patch all needed files and install Lua mod.
        If using '--force', discard backups, hashes and SJSON data, and uninstall Lua mod."""
        scaling, hud = helpers.autodetect(width, height, scaling, hud)
        helpers.configure_screen_variables(width, height, scaling)
        LOGGER.info(f"Using resolution: {config.resolution.width, config.resolution.height}")
        LOGGER.info(f"Using '--scaling={scaling}': computed patch viewport {config.new_screen.width, config.new_screen.height}")

        config.center_hud = True if hud == HUD.CENTER else False
        msg = f"Using '--hud={hud}': HUD will be kept in the center of the screen" if config.center_hud else f"Using '--hud={hud}': HUD will be expanded horizontally / vertically"
        LOGGER.info(msg)

        if not custom_resolution:
            LOGGER.info("Using '--no-custom-resolution': will not bypass monitor resolution detection")
        config.custom_resolution = custom_resolution

        if force:
            LOGGER.info("Using '--force': will repatch on top of existing files in case of hash mismatch and store new backups / hashes")
            config.force = True

        # run 'modimporter --clean' (if available) to restore everything before patching
        if config.modimporter:
            LOGGER.info(f"Running 'modimporter --clean' to restore original state before patching")
            helpers.run_modimporter(clean_only=True) 

        try:
            patchers.patch_engines()
            patchers.patch_sjsons()
            patchers.patch_profile_sjsons()
            lua_mod.install()
        except hashes.HashMismatch as e:
            LOGGER.error(e)
            if config.interactive_mode:
                LOGGER.error("It looks like the game was updated. Do you wish to discard previous backups and re-patch Hades from its current state?")
                choice = interactive.pick(options=['Yes', 'No',], recommended_option='Yes', additional_option=None)
                if choice == 'Yes':
                    self.handler(width, height, scaling, hud, custom_resolution, force=True)
            else:
                LOGGER.error("Was the game updated? Re-run with '--force' to discard previous backups and re-patch Hades from its current state.")
        except (LookupError, FileExistsError) as e:
            LOGGER.error(e)


class RestoreSubcommand(BaseSubcommand):
    def __init__(self, **kwargs) -> None:
        super().__init__(description="restore Hades to its pre-Hephaistos state", **kwargs)

    def handler(self, **kwargs) -> None:
        """Restore backups, discard hashes and SJSON data, uninstall Lua mod."""
        # run 'modimporter --clean' (if available) to unregister Hephaistos
        if config.modimporter:
            LOGGER.info(f"Running 'modimporter --clean' to unregister Hephaistos")
            helpers.run_modimporter(clean_only=True)
        backups.restore()
        hashes.discard()
        sjson_data.discard()
        lua_mod.uninstall()
        # clean up Hephaistos data dir if empty (using standalone executable)
        if not any(config.HEPHAISTOS_DATA_DIR.iterdir()):
            dir_util.remove_tree(str(config.HEPHAISTOS_DATA_DIR))
            LOGGER.info(f"Cleaned up empty directory '{config.HEPHAISTOS_DATA_DIR}'")
        # re-run modimporter (if available) to re-register other mods
        if config.modimporter:
            LOGGER.info(f"Running 'modimporter' to re-register other mods")
            helpers.run_modimporter()


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
        hades_engine_checks = [
            patchers.patch_engines_status(),
        ]
        hades_lua_checks = [
            lua_mod.status(),
        ]
        if all(hephaistos_data_checks) and all(hades_engine_checks) and all(hades_lua_checks):
            print(f"Hades looks correctly patched with Hephaistos.")
        elif all(hephaistos_data_checks) and all(hades_engine_checks) and config.modimporter:
            print(f"Hades was patched with Hephaistos, but Lua hook not found in Hades files. Was there an error while running 'modimporter'? Try to re-run 'modimporter' or re-patch Hephaistos.")
        elif all(hephaistos_data_checks):
            print(f"Hades was patched with Hephaistos, but Hades files were modified. Was the game updated?")
        else:
            print(f"Hades is not patched with Hephaistos.")


class VersionSubcommand(BaseSubcommand):
    def __init__(self, **kwargs) -> None:
        super().__init__(description="check Hephaistos version and if an update is available", **kwargs)

    def handler(self, **kwargs) -> None:
        """Check Hephaistos version and if an update is available."""
        print(helpers.check_version())
