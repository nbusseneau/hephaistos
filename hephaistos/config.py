import logging
from pathlib import Path

from hephaistos.helpers import Viewport


# Hades default screen size
DEFAULT_VIRTUAL_VIEWPORT = (1920, 1080)
DEFAULT_WIDTH, DEFAULT_HEIGHT = DEFAULT_VIRTUAL_VIEWPORT
DEFAULT_CENTER_X, DEFAULT_CENTER_Y = (int(DEFAULT_WIDTH / 2), int(DEFAULT_HEIGHT / 2))

# Hephaistos constants
HEPHAISTOS_NAME = 'hephaistos'
LOGGER = logging.getLogger(HEPHAISTOS_NAME)
HEPHAISTOS_DATA_DIR = Path(HEPHAISTOS_NAME + '-data')

# Hephaistos variables
interactive_mode = False
hades_dir: Path = None
new_viewport: Viewport = None
new_width: int
new_height: int
new_center_x: int
new_center_y: int
scale_factor_X: float = None
scale_factor_Y: float = None
scale_factor: float = None
