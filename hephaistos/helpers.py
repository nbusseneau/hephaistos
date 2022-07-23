import contextlib
from enum import Enum
import importlib.util
import json
import logging
import os
import os.path
from pathlib import Path
import platform
import re
import subprocess
from typing import Union
import urllib.error
import urllib.request

import sjson

from hephaistos import config
from hephaistos.config import LOGGER


# Type definitions
IntOrFloat = Union[int, float]
class Scaling(str, Enum):
    AUTODETECT = 'autodetect'
    HOR_PLUS = 'hor+'
    VERT_PLUS = 'vert+'
    PIXEL_BASED = 'pixel'
class HUD(str, Enum):
    EXPAND = 'expand'
    CENTER = 'center'
class Platform(str, Enum):
    WINDOWS = 'Windows'
    MS_STORE = 'Windows (Microsoft Store)'
    MACOS = 'macOS'
    LINUX = 'Linux'


# Set up platform depending on detected OS. If we are on Windows, this might be
# overriden later if we detect a Microsoft Store version of Hades.
if platform.system() == 'Darwin': config.platform = Platform.MACOS
elif platform.system() == 'Linux': config.platform = Platform.LINUX
else: config.platform = Platform.WINDOWS


HADES_DIR_EXPECTED_ITEMS = {
    Platform.WINDOWS: ['Content', 'x64', 'x64Vk', 'x86'],
    Platform.MS_STORE: ['Content', 'E0A69B86-F3DD-416D-BCA8-3782255B0B74'],
    Platform.MACOS: ['Game.macOS.app'],
}
# Steam on Linux uses Proton to wrap around the Windows version
HADES_DIR_EXPECTED_ITEMS[Platform.LINUX] = HADES_DIR_EXPECTED_ITEMS[Platform.WINDOWS]


def is_valid_hades_dir(hades_dir: Path, fail_on_not_found: bool=True) -> bool:
    """Check if given directory is indeed Hades by looking at its contents."""
    # If on Windows, do a first check to determine if this is actually the
    # Microsoft Store version
    if config.platform == Platform.WINDOWS and all(hades_dir.joinpath(item).exists() for item in HADES_DIR_EXPECTED_ITEMS[Platform.MS_STORE]):
        config.platform = Platform.MS_STORE
        return True
    # Check existence of expected items for the current platform
    if all(hades_dir.joinpath(item).exists() for item in HADES_DIR_EXPECTED_ITEMS[config.platform]):
        return True
    else:
        if fail_on_not_found:
            raise HadesNotFound(f"Did not find expected items {HADES_DIR_EXPECTED_ITEMS[config.platform]} in '{hades_dir}'")
        return False


class HadesNotFound(FileNotFoundError): ...


TRY_STEAM = {
    Platform.WINDOWS: [
        os.path.expandvars(r'%programfiles%\Steam\steamapps'),
        os.path.expandvars(r'%programfiles(x86)%\Steam\steamapps'),
    ],
    Platform.MACOS: [
        os.path.expanduser(r'~/Library/Application Support/Steam/SteamApps'),
    ],
    Platform.LINUX: [ # Proton wrapper library path
        os.path.expanduser(r'~/.steam/steam/steamapps'),
    ],
}
LIBRARY_REGEX = re.compile(r'"path"\s+"(.*)"')


TRY_EPIC = {
    Platform.WINDOWS: [
        os.path.expandvars(r'%programdata%\Epic\EpicGamesLauncher\Data\Manifests'),
    ],
    Platform.MACOS: [
        os.path.expanduser(r'~/Library/Application Support/Epic/EpicGamesLauncher/Data/Manifests'),
    ],
    Platform.LINUX: [], # Epic Games does not have a Linux version
}
DISPLAY_NAME_REGEX = re.compile(r'"DisplayName": "(.*)"')
INSTALL_LOCATION_REGEX = re.compile(r'"InstallLocation": "(.*)"')


def try_detect_hades_dirs() -> list[Path]:
    """Try to detect Hades directory from Steam and Epic Games files."""
    potential_hades_dirs: list[Path] = []
    for steam_library_file in [Path(item).joinpath('libraryfolders.vdf') for item in TRY_STEAM[config.platform]]:
        if steam_library_file.exists():
            LOGGER.debug(f"Found Steam library file at '{steam_library_file}'")
            for steam_library in LIBRARY_REGEX.finditer(steam_library_file.read_text()):
                potential_hades_dirs.append(Path(steam_library.group(1)).joinpath('steamapps/common/Hades'))
    for epic_metadata_dir in [Path(item) for item in TRY_EPIC[config.platform]]:
        for epic_metadata_item in epic_metadata_dir.glob('*.item'):
            item = epic_metadata_item.read_text()
            search_name = DISPLAY_NAME_REGEX.search(item)
            if search_name and 'Hades' in search_name.group(1):
                LOGGER.debug(f"Found potential Epic Games' Hades installation from '{epic_metadata_item}'")
                potential_hades_dirs.append(Path(INSTALL_LOCATION_REGEX.search(item).group(1)))
    return [hades_dir for hades_dir in potential_hades_dirs if hades_dir.exists() and is_valid_hades_dir(hades_dir, False)]


def __try_windows_save_dirs() -> list[Path]:
    # Windows (Steam / Epic Games) might store saves:
    # - Directly inside the Documents directory
    # - Nested inside OneDrive inside the Documents directory
    save_dirs = [ 
        r'Saved Games\Hades',
        r'OneDrive\Saved Games\Hades',
    ]
    # Try to detect actual path to Documents folder from registry, in case user
    # has moved its Documents folder somewhere else than `%USERDIR%\Documents`
    try:
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            my_documents_path = winreg.QueryValueEx(key, r'Personal')[0]
        LOGGER.debug(f"Detected 'Documents' path from registry: {my_documents_path}")
        save_dirs = [Path(my_documents_path).joinpath(item) for item in save_dirs]
    # Fall back to default `%USERDIR%\Documents` value if no registry entry
    # found or anything goes wrong
    except Exception as e:
        LOGGER.debug(f"Could not detect 'Documents' path from registry.")
        LOGGER.debug(e, exc_info=True)
        save_dirs = [Path(os.path.expanduser(r'~\Documents')).joinpath(item) for item in save_dirs]
    return save_dirs


def __try_ms_store_save_dirs() -> list[Path]:
    # Microsoft Store version stores save files in the UWP app storage
    # The save files themselves are nested somewhere in a sub-directory with
    # random hexadecimal names for both directories names and files
    save_dirs = [
        r'~\AppData\Local\Packages\SupergiantGamesLLC.Hades_q53c1yqmx7pha\SystemAppData\wgs',
    ]
    return [Path(os.path.expanduser(item)) for item in save_dirs]


def __try_macos_save_dirs() -> list[Path]:
    save_dirs = [
        r'~/Library/Application Support/Supergiant Games/Hades',
    ]
    return [Path(os.path.expanduser(item)) for item in save_dirs]


def __try_linux_save_dirs() -> list[Path]:
    # Proton wrapper save file path is relative to Hades dir
    # e.g. if Hades dir => /path/to/SteamLibrary/steamapps/common/Hades
    # then save dir => /path/to/SteamLibrary/steamapps/compatdata/1145360/pfx/drive_c/users/steamuser/Documents/Saved Games/Hades
    save_dirs = [
        r'../../compatdata/1145360/pfx/drive_c/users/steamuser/Documents/Saved Games/Hades',
    ]
    return [Path(config.hades_dir).joinpath(item) for item in save_dirs]


TRY_SAVE_DIR = {
    Platform.WINDOWS: __try_windows_save_dirs,
    Platform.MS_STORE: __try_ms_store_save_dirs,
    Platform.MACOS: __try_macos_save_dirs,
    Platform.LINUX: __try_linux_save_dirs,
}


def try_get_profile_sjson_files() -> list[Path]:
    """Try to detect save directory and list all Profile*.sjson files."""
    save_dirs = TRY_SAVE_DIR[config.platform]()
    for save_dir in save_dirs:
        if save_dir.exists():
            LOGGER.debug(f"Found save directory at '{save_dir}'")
            if config.platform == Platform.MS_STORE:
                # Microsoft Store save files are not actually named
                # `Profile*.sjson` and instead use random hexadecimal names with
                # no file extensions, so we need to list them by trying to parse
                # them as SJSON
                profiles = __find_sjsons(save_dir)
            else:
                profiles = [item for item in save_dir.glob('Profile*.sjson')]
            if profiles:
                return profiles
    save_dirs_list = '\n'.join(f"  - {save_dir}" for save_dir in save_dirs)
    msg = f"""Did not find any 'ProfileX.sjson' in save directories:
{save_dirs_list}"""
    LOGGER.warning(msg)
    return []


def __find_sjsons(save_dir: Path) -> list[Path]:
    """Find actual SJSON files in directory."""
    LOGGER.debug(f"Detecting SJSON files from '{save_dir}'")
    sjsons: list[Path] = []
    for file in save_dir.rglob('*'):
        try:
            sjson.loads(Path(file).read_text())
            LOGGER.debug(f"Found valid SJSON in '{file}'")
            sjsons.append(file)
        except:
            pass
    return sjsons


VERSION_CHECK_ERROR = "could not check latest version -- perhaps no Internet connection is available?"


def check_version() -> str:
    """Compare current version with latest GitHub release."""
    try:
        LOGGER.debug(f"Checking latest version at {config.LATEST_RELEASE_URL}")
        request = urllib.request.Request(config.LATEST_RELEASE_API_URL)
        response = urllib.request.urlopen(request).read()
        data = json.loads(response.decode('utf-8'))
        latest_version = data['name']
    except urllib.error.URLError as e:
        LOGGER.debug(e, exc_info=True)
        latest_version = VERSION_CHECK_ERROR
    msg = f"""Current version: {config.VERSION}
Latest version: {latest_version}"""
    if latest_version != config.VERSION and latest_version != VERSION_CHECK_ERROR:
        msg += f"\nA new version of Hephaistos is available at: {config.LATEST_RELEASE_URL}"
    return msg


MOD_IMPORTERS = [
    'modimporter.py', # Python version
    'modimporter.exe', # Windows version
    'modimporter', # macOS / Linux version
]


def try_get_modimporter() -> Path:
    """Check if modimporter is available in the Content directory."""
    for mod_importer in MOD_IMPORTERS:
        modimporter = config.content_dir.joinpath(mod_importer)
        if modimporter.exists():
            LOGGER.info(f"'modimporter' detected at '{modimporter}'")
            return modimporter
    return None


@contextlib.contextmanager
def remember_cwd():
    """Store current working directory on context enter and restore on exit."""
    cwd = os.getcwd()
    try:
        yield
    finally:
        os.chdir(cwd)


class ModImporterRuntimeError(RuntimeError): ...


def run_modimporter(modimporter_file: Path, clean_only: bool=False) -> None:
    """Run modimporter from the Content directory, as if the user did it."""
    with remember_cwd():
        # temporarily switch to modimporter working dir (Content)
        os.chdir(modimporter_file.parent)
        # dynamically import modimporter.py if using Python version
        if modimporter_file.suffix == '.py':
            try:
                spec = importlib.util.spec_from_file_location("modimporter", modimporter_file.name)
                modimporter = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modimporter)
                modimporter.game = 'Hades'
                modimporter.clean_only = clean_only
                modimporter.LOGGER.setLevel(logging.ERROR)
                modimporter.start()
            except AttributeError as e:
                LOGGER.error(e)
                raise ModImporterRuntimeError("Failed to import 'modimporter.py': your copy of 'modimporter.py' is likely outdated, please update it (a version >= 1.3.0 is required)")
        # otherwise execute modimporter directly if using binary version
        else:
            args = [modimporter_file.name, '--no-input', '--quiet', '--game', 'Hades']
            if clean_only:
                args += ['--clean']
            try:
                subprocess.run(args, check=True, text=True, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                if "unrecognized arguments" in e.stderr:
                    LOGGER.error(e)
                    raise ModImporterRuntimeError("Failed to import 'modimporter.py': your copy of 'modimporter.py' is likely outdated, please update it (a version >= 1.3.0 is required)")
                else:
                    raise e


def configure_screen_variables(width: int, height: int, scaling: Scaling) -> Scaling:
    """Compute virtual viewport size to patch depending on scaling type and given resolution width / height."""
    if scaling == Scaling.AUTODETECT:
        # use hor+ for aspect ratios wider than default (e.g. 21:9)
        if (width / height) >= (config.DEFAULT_SCREEN.width / config.DEFAULT_SCREEN.height):
            scaling = Scaling.HOR_PLUS
        # use vert+ for aspect ratios taller than default (e.g. 16:10)
        else:
            scaling = Scaling.VERT_PLUS
    config.resolution = config.Screen(width, height)
    if scaling == Scaling.HOR_PLUS:
        virtual_width = int(width / height * config.DEFAULT_SCREEN.height)
        config.new_screen = config.Screen(virtual_width, config.DEFAULT_SCREEN.height)
    elif scaling == Scaling.VERT_PLUS:
        virtual_height = int(height / width * config.DEFAULT_SCREEN.width)
        config.new_screen = config.Screen(config.DEFAULT_SCREEN.width, virtual_height)
    elif scaling == Scaling.PIXEL_BASED:
        config.new_screen = config.Screen(width, height)
    else:
        raise ValueError("Unknown scaling type")
    config.scale_factor_X = config.new_screen.width / config.DEFAULT_SCREEN.width
    config.scale_factor_Y = config.new_screen.height / config.DEFAULT_SCREEN.height
    config.scale_factor = max(config.scale_factor_X, config.scale_factor_Y)
    return scaling


def recompute_fixed_value(original_value: IntOrFloat, original_reference_point: IntOrFloat, new_reference_point: IntOrFloat) -> IntOrFloat:
    """Recompute a fixed value, i.e. a value that was set at an offset from a
    reference point. Used for moving around elements with a fixed size or fixed
    position.

    Examples:

    - Recompute X value fixed at an offset of 60 from the center of the screen:
            recompute_fixed_value(1020, 960, 1296) = 1356
    - Recompute Y value fixed at an offset of -80 from the bottom of the screen:
            recompute_fixed_value(1000, 1080, 1600) = 1520
    """
    offset = original_reference_point - original_value
    return new_reference_point - offset


def recompute_fixed_X_from_left(original_value: IntOrFloat, center_hud: bool=None) -> IntOrFloat:
    if center_hud is None:
        center_hud = config.center_hud
    return recompute_fixed_X_from_center(original_value) if center_hud else original_value


def recompute_fixed_X_from_center(original_value: IntOrFloat) -> IntOrFloat:
    return recompute_fixed_value(original_value, config.DEFAULT_SCREEN.center_x, config.new_screen.center_x)


def recompute_fixed_X_from_right(original_value: IntOrFloat, center_hud: bool=None) -> IntOrFloat:
    if center_hud is None:
        center_hud = config.center_hud
    return recompute_fixed_X_from_center(original_value) \
        if center_hud \
        else recompute_fixed_value(original_value, config.DEFAULT_SCREEN.width, config.new_screen.width)


def recompute_fixed_Y_from_top(original_value: IntOrFloat, center_hud: bool=None) -> IntOrFloat:
    if center_hud is None:
        center_hud = config.center_hud
    return recompute_fixed_Y_from_center(original_value) if center_hud else original_value


def recompute_fixed_Y_from_center(original_value: IntOrFloat) -> IntOrFloat:
    return recompute_fixed_value(original_value, config.DEFAULT_SCREEN.center_y, config.new_screen.center_y)


def recompute_fixed_Y_from_bottom(original_value: IntOrFloat, center_hud: bool=None) -> IntOrFloat:
    if center_hud is None:
        center_hud = config.center_hud
    return recompute_fixed_Y_from_center(original_value) \
        if center_hud \
        else recompute_fixed_value(original_value, config.DEFAULT_SCREEN.height, config.new_screen.height)


def rescale_X(original_value: IntOrFloat) -> float:
    return original_value * config.scale_factor_X


def rescale_Y(original_value: IntOrFloat) -> float:
    return original_value * config.scale_factor_Y


def rescale(original_value: IntOrFloat) -> float:
    return original_value * config.scale_factor


def capitalize(value: str) -> str:
    return value[:1].upper() + value[1:]
