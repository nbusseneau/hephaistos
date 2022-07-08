from dataclasses import dataclass
import logging
from pathlib import Path
import sys


@dataclass(frozen=True)
class Screen:
    width: int
    height: int

    @property
    def center_x(self) -> int:
        return int(self.width / 2)

    @property
    def center_y(self) -> int:
        return int(self.height / 2)


# Hades default screen size
DEFAULT_SCREEN = Screen(1920, 1080)

# Hephaistos constants
VERSION = 'v1.7.0'
LATEST_RELEASE_URL = 'https://github.com/nbusseneau/hephaistos/releases/latest/'
LATEST_RELEASE_API_URL = 'https://api.github.com/repos/nbusseneau/hephaistos/releases/latest'
HEPHAISTOS_NAME = 'hephaistos'
LOGGER = logging.getLogger(HEPHAISTOS_NAME)
HEPHAISTOS_DATA_DIR = Path(HEPHAISTOS_NAME + '-data')
BACKUP_DIR = HEPHAISTOS_DATA_DIR.joinpath('backups')
HASH_DIR = HEPHAISTOS_DATA_DIR.joinpath('hashes')
# If running from PyInstaller, get Lua mod source files from bundled data
# otherwise get from regular `hephaistos-data` folder
MOD_SOURCE_DIR = Path(getattr(sys, '_MEIPASS', '.')).joinpath(HEPHAISTOS_DATA_DIR).joinpath('lua')
SJSON_DATA_DIR = HEPHAISTOS_DATA_DIR.joinpath('sjson-data')
SJSON_SUFFIX = '.sjson'

# Hephaistos variables
platform = None
interactive_mode = False
force = False
hades_dir: Path
content_dir: Path
resolution: Screen
custom_resolution = True
new_screen: Screen
scale_factor_X: float
scale_factor_Y: float
scale_factor: float
center_hud = False
modimporter: Path = None
