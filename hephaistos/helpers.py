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
        (virtual_width, virtual_height) = config.DEFAULT_VIRTUAL_VIEWPORT
        virtual_width = int(width / height * virtual_height)
        return (virtual_width, virtual_height)
    elif scaling == Scaling.PIXEL_BASED:
        return (width, height)
    else:
        raise ValueError("Unknown scaling type")


def recompute_fixed_value(original_value: IntOrFloat, original_width_or_height: IntOrFloat, new_width_or_height: IntOrFloat, threshold: IntOrFloat) -> IntOrFloat:
    """Recompute a fixed value, i.e. a value that was set at an offset from a
    reference point defined depending on a threshold. Used for moving around
    elements with a fixed size or fixed position.

    Examples:

    - Recompute X value fixed at an offset of 60 from the center of the screen:
        recompute_fixed_value(1020, 960, 1296, 150) = 1356
    - Recompute Y value fixed at an offset of -80 from the bottom of the screen:
        recompute_fixed_value(1000, 1080, 1600, 150) = 1520
    """
    original_center = original_width_or_height / 2
    new_center = new_width_or_height / 2
    cutoff = original_width_or_height - threshold
    LOGGER.debug(f'[input] original value: {original_value} | original w/h: {original_width_or_height}, new w/h: {new_width_or_height}, threshold: {threshold}')
    LOGGER.debug(f'[computed] original center: {original_center} | new center: {new_center}, cutoff: {cutoff}')
    # X: fixed offset from the left, Y: fixed offset from the top
    if 0 <= original_value <= threshold:
        LOGGER.debug(f'[fixed left/top] untouched')
        return original_value
    # X and Y: fixed offset from the center
    elif threshold < original_value < cutoff:
        new_value = original_value + (new_center - original_center)
        LOGGER.debug(f'[fixed from center] new value: {new_value}')
        return new_value if isinstance(original_value, float) else int(new_value)
    # X: fixed offset from the right, Y: fixed offset from the bottom
    elif cutoff <= original_value <= original_width_or_height:
        new_value = original_value + (new_width_or_height - original_width_or_height)
        LOGGER.debug(f'[fixed from right/bottom] new value: {new_value}')
        return new_value if isinstance(original_value, float) else int(new_value)


def recompute_fixed_X(original_value: IntOrFloat) -> IntOrFloat:
    return recompute_fixed_value(original_value, config.DEFAULT_WIDTH, config.new_viewport[0], config.FIXED_ALIGN_THRESHOLD)


def recompute_fixed_Y(original_value: IntOrFloat) -> IntOrFloat:
    return recompute_fixed_value(original_value, config.DEFAULT_HEIGHT, config.new_viewport[1], config.FIXED_ALIGN_THRESHOLD)


# Source: https://code.activestate.com/recipes/134892/
# Modifications:
# - Added .decode() to Windows getch()
# - Removed unused import in Unix __init__
class _Getch:
    """Gets a single character from standard input. Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self): ...
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch().decode()


getch = _Getch()


CANCEL_OPTION='Cancel'


def interactive_pick(prompt: str="Pick an option:", options: Union[OrderedDict, list]=None, *args, **kwargs) -> Any:
    if not options and kwargs:
        options = OrderedDict(kwargs)
    if isinstance(options, OrderedDict):
        options[CANCEL_OPTION] = CANCEL_OPTION
    elif CANCEL_OPTION not in options:
        options.append(CANCEL_OPTION)
    print(prompt)
    index_key_dict = {index + 1: key for index, key in enumerate(options)}
    for index, key in index_key_dict.items():
        print(f"{index}. {options[key]}") if isinstance(options, OrderedDict) else print(f"{index}. {key}")
    print("Choice: ", end='', flush=True)
    char = getch()
    print(char + '\n')
    try:
        option = int(char)
        value = index_key_dict[option]
        if value == CANCEL_OPTION:
            raise InteractiveModeCancelled()
        return index_key_dict[option]
    except (ValueError, KeyError):
        return interactive_pick("Please input a valid number from the given list:", options)


class InteractiveModeCancelled(RuntimeError): ...
