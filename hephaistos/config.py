from hephaistos.helpers import Viewport
from pathlib import Path


# Hades default screen size
DEFAULT_VIRTUAL_VIEWPORT = (1920, 1080)
DEFAULT_WIDTH, DEFAULT_HEIGHT = DEFAULT_VIRTUAL_VIEWPORT

# Hephaistos constants
HEPHAISTOS_DIR = Path('hephaistos')
FIXED_ALIGN_THRESHOLD = 150

# Hephaistos variables
hades_dir: Path = None
new_viewport: Viewport = None
