import logging
from pathlib import Path


# Hades default screen size
DEFAULT_VIRTUAL_VIEWPORT = (1920, 1080)
DEFAULT_WIDTH, DEFAULT_HEIGHT = DEFAULT_VIRTUAL_VIEWPORT
DEFAULT_CENTER_X, DEFAULT_CENTER_Y = (int(DEFAULT_WIDTH / 2), int(DEFAULT_HEIGHT / 2))

# Hephaistos constants
VERSION = 'v1.3.2'
LATEST_RELEASE_URL = 'https://github.com/nbusseneau/hephaistos/releases/latest/'
LATEST_RELEASE_API_URL = 'https://api.github.com/repos/nbusseneau/hephaistos/releases/latest'
HEPHAISTOS_NAME = 'hephaistos'
LOGGER = logging.getLogger(HEPHAISTOS_NAME)
HEPHAISTOS_DATA_DIR = Path(HEPHAISTOS_NAME + '-data')

# Hephaistos variables
interactive_mode = False
hades_dir: Path
new_width: int
new_height: int
new_center_x: int
new_center_y: int
scale_factor_X: float
scale_factor_Y: float
scale_factor: float
center_hud = False
resolution_width: int
resolution_height: int
custom_resolution = False
