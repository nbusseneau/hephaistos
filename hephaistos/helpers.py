from collections import OrderedDict
from enum import Enum
import logging
from pathlib import Path
import re
from typing import Any, Tuple, Union

from hephaistos import config


# Helpers logging is not really useful outside of development, so it gets its
# own logger for tweaking log level separately
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARNING)

# Type definitions
Viewport = Tuple[int, int]
IntOrFloat = Union[int, float]
SJSON = Union[OrderedDict, list, str, IntOrFloat, Any]


class Scaling(str, Enum):
    HOR_PLUS = 'hor+'
    PIXEL_BASED = 'pixel'


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
    r'C:\Program Files (x86)\Steam\steamapps',
    r'~/Library/Application Support/Steam/SteamApps/',
    r'~/.steam/steam/steamapps/',
]
LIBRARY_REGEX = re.compile(r'"\d"\s+"(.*)"')
TRY_EPIC = [
    r'C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests',
    r'~/Library/Application Support/Epic/EpicGamesLauncher/Data/Manifests',
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
                potential_hades_dirs.append(Path(INSTALL_LOCATION_REGEX.search(item).group(1)))
    return [hades_dir for hades_dir in potential_hades_dirs if hades_dir.exists() and is_valid_hades_dir(hades_dir, False)]


def compute_viewport(width: int, height: int, scaling: Scaling) -> None:
    """Compute virtual viewport size to patch depending on scaling type and display resolution width / height."""
    if scaling == Scaling.HOR_PLUS:
        virtual_width = int(width / height * config.DEFAULT_HEIGHT)
        config.new_viewport = (virtual_width, config.DEFAULT_HEIGHT)
    elif scaling == Scaling.PIXEL_BASED:
        config.new_viewport = (width, height)
    else:
        raise ValueError("Unknown scaling type")
    config.new_width, config.new_height = config.new_viewport
    config.new_center_x, config.new_center_y = (int(config.new_width / 2), int(config.new_height / 2))
    config.scale_factor_X = config.new_width / config.DEFAULT_WIDTH
    config.scale_factor_Y = config.new_height / config.DEFAULT_HEIGHT
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


def recompute_fixed_X_from_center(original_value: IntOrFloat) -> IntOrFloat:
    return recompute_fixed_value(original_value, config.DEFAULT_CENTER_X, config.new_center_x)


def recompute_fixed_X_from_right(original_value: IntOrFloat) -> IntOrFloat:
    return recompute_fixed_value(original_value, config.DEFAULT_WIDTH, config.new_width)


def recompute_fixed_Y_from_center(original_value: IntOrFloat) -> IntOrFloat:
    return recompute_fixed_value(original_value, config.DEFAULT_CENTER_Y, config.new_center_y)


def recompute_fixed_Y_from_bottom(original_value: IntOrFloat) -> IntOrFloat:
    return recompute_fixed_value(original_value, config.DEFAULT_HEIGHT, config.new_height)


def rescale_X(original_value: IntOrFloat) -> float:
    return original_value * config.scale_factor_X


def rescale_Y(original_value: IntOrFloat) -> float:
    return original_value * config.scale_factor_Y


def rescale(original_value: IntOrFloat) -> float:
    return original_value * config.scale_factor
