import logging
from pathlib import Path

from hephaistos.helpers import Viewport


# Hades default screen size
DEFAULT_VIRTUAL_VIEWPORT = (1920, 1080)
DEFAULT_WIDTH, DEFAULT_HEIGHT = DEFAULT_VIRTUAL_VIEWPORT

# Hephaistos constants
HEPHAISTOS_NAME = 'hephaistos'
LOGGER = logging.getLogger(HEPHAISTOS_NAME)
HEPHAISTOS_DATA_DIR = Path(HEPHAISTOS_NAME + '-data')
FIXED_ALIGN_THRESHOLD = 115

# Hephaistos variables
hades_dir: Path = None
new_viewport: Viewport = None
interactive_mode = False
