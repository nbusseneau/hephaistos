from enum import Enum
import json
import logging
import os.path
from pathlib import Path
import re
from typing import Union
import urllib.error
import urllib.request

from hephaistos import config


# Helpers logging is not really useful outside of development, so it gets its
# own logger for tweaking log level separately
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARNING)

# Type definitions
IntOrFloat = Union[int, float]
class Scaling(str, Enum):
    HOR_PLUS = 'hor+'
    PIXEL_BASED = 'pixel'
class HUD(str, Enum):
    EXPAND = 'expand'
    CENTER = 'center'


HADES_DIR_DIRS = ['Content', 'x64', 'x64Vk', 'x86']


def is_valid_hades_dir(dir: Path, fail_on_not_found: bool=True):
    for item in HADES_DIR_DIRS:
        directory = dir.joinpath(item)
        if not directory.exists():
            if fail_on_not_found:
                raise HadesNotFound(f"Did not find expected directory '{item}' in '{dir}'")
            return False
    return True


class HadesNotFound(FileNotFoundError): ...


TRY_STEAM = [
    os.path.expandvars(r'%programfiles%\Steam\steamapps'),
    os.path.expandvars(r'%programfiles(x86)%\Steam\steamapps'),
    os.path.expanduser(r'~/Library/Application Support/Steam/SteamApps'),
    os.path.expanduser(r'~/.steam/steam/steamapps'),
]
LIBRARY_REGEX = re.compile(r'"path"\s+"(.*)"')
TRY_EPIC = [
    os.path.expandvars(r'%programdata%\Epic\EpicGamesLauncher\Data\Manifests'),
    os.path.expanduser(r'~/Library/Application Support/Epic/EpicGamesLauncher/Data/Manifests'),
]
DISPLAY_NAME_REGEX = re.compile(r'"DisplayName": "(.*)"')
INSTALL_LOCATION_REGEX = re.compile(r'"InstallLocation": "(.*)"')


def try_detect_hades_dirs():
    potential_hades_dirs: list[Path] = []
    for steam_library_file in [Path(item).joinpath('libraryfolders.vdf') for item in TRY_STEAM]:
        if steam_library_file.exists():
            LOGGER.debug(f"Found Steam library file at '{steam_library_file}'")
            for steam_library in LIBRARY_REGEX.finditer(steam_library_file.read_text()):
                potential_hades_dirs.append(Path(steam_library.group(1)).joinpath('steamapps/common/Hades'))
    for epic_metadata_dir in [Path(item) for item in TRY_EPIC]:
        for epic_metadata_item in epic_metadata_dir.glob('*.item'):
            item = epic_metadata_item.read_text()
            search_name = DISPLAY_NAME_REGEX.search(item)
            if search_name and 'Hades' in search_name.group(1):
                LOGGER.debug(f"Found potential Epic Games' Hades installation from '{epic_metadata_item}'")
                potential_hades_dirs.append(Path(INSTALL_LOCATION_REGEX.search(item).group(1)))
    return [hades_dir for hades_dir in potential_hades_dirs if hades_dir.exists() and is_valid_hades_dir(hades_dir, False)]


SAVE_DIRECTORY = {
    os.path.expanduser(r'~\Documents\Saved Games\Hades'),
    os.path.expanduser(r'~/Library/Application Support/Supergiant Games/Hades'),
    os.path.expanduser(r'~/.steam/steam/steamapps/compatdata/1145360/pfx/drive_c/users/steamuser/Documents/Saved Games/Hades'),
}


def try_get_profile_sjson_files():
    for save_dir in [Path(item) for item in SAVE_DIRECTORY]:
        if save_dir.exists():
            LOGGER.debug(f"Found save directory at '{save_dir}'")
            return [item for item in save_dir.glob('Profile*.sjson')]


VERSION_CHECK_ERROR = "could not check latest version -- perhaps no Internet connection is available?"


def check_version() -> str:
    try:
        config.LOGGER.debug(f"Checking latest version at {config.LATEST_RELEASE_URL}")
        request = urllib.request.Request(config.LATEST_RELEASE_API_URL)
        response = urllib.request.urlopen(request).read()
        data = json.loads(response.decode('utf-8'))
        latest_version = data['name']
    except urllib.error.URLError as e:
        config.LOGGER.debug(e, stack_info=True)
        latest_version = VERSION_CHECK_ERROR
    msg = f"""Current version: {config.VERSION}
Latest version: {latest_version}"""
    if latest_version != config.VERSION and latest_version != VERSION_CHECK_ERROR:
        msg += f"\nA new version of Hephaistos is available at: {config.LATEST_RELEASE_URL}"
    return msg


def configure_screen_variables(width: int, height: int, scaling: Scaling) -> None:
    """Compute virtual viewport size to patch depending on scaling type and display resolution width / height."""
    config.resolution = config.Screen(width, height)
    if scaling == Scaling.HOR_PLUS:
        virtual_width = int(width / height * config.DEFAULT_SCREEN.height)
        config.new_screen = config.Screen(virtual_width, config.DEFAULT_SCREEN.height)
    elif scaling == Scaling.PIXEL_BASED:
        config.new_screen = config.Screen(width, height)
    else:
        raise ValueError("Unknown scaling type")
    config.scale_factor_X = config.new_screen.width / config.DEFAULT_SCREEN.width
    config.scale_factor_Y = config.new_screen.height / config.DEFAULT_SCREEN.height
    config.scale_factor = max(config.scale_factor_X, config.scale_factor_Y)


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


def recompute_fixed_Y_from_center(original_value: IntOrFloat) -> IntOrFloat:
    return recompute_fixed_value(original_value, config.DEFAULT_SCREEN.center_y, config.new_screen.center_y)


def recompute_fixed_Y_from_bottom(original_value: IntOrFloat) -> IntOrFloat:
    return recompute_fixed_value(original_value, config.DEFAULT_SCREEN.height, config.new_screen.height)


def rescale_X(original_value: IntOrFloat) -> float:
    return original_value * config.scale_factor_X


def rescale_Y(original_value: IntOrFloat) -> float:
    return original_value * config.scale_factor_Y


def rescale(original_value: IntOrFloat) -> float:
    return original_value * config.scale_factor


def capitalize(value: str) -> str:
    return value[:1].upper() + value[1:]
