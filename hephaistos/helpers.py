from collections import OrderedDict
from enum import Enum
import logging
from pathlib import Path
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


def get_hades_dir(hades_dir: str):
    # check that we're in the right place
    # if not, try to detect where Hades is and propose user to patch there
    return Path(hades_dir)


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
