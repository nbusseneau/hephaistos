from distutils import dir_util
import logging
from pathlib import Path
import re

from hephaistos import config, patchers


logger = logging.getLogger(__name__)
MOD_SOURCE_DIR = config.HEPHAISTOS_DIR.joinpath('lua')
HADES_MOD_DIR = 'Content/Mods/Hephaistos'
MOD_ENTRY_POINT = 'Hephaistos.lua'
MOD_CONFIG_FILE = 'HephaistosConfig.lua'
WIDTH_REGEX = re.compile(r'(Hephaistos.ScreenWidth = )\d+')
HEIGHT_REGEX = re.compile(r'(Hephaistos.ScreenHeight = )\d+')


def install() -> None:
    mod_dir = config.hades_dir.joinpath(HADES_MOD_DIR)
    mod_dir.mkdir(parents=True, exist_ok=True)
    dir_util.copy_tree(str(MOD_SOURCE_DIR), str(mod_dir))
    logger.info(f"Installed Lua mod '{MOD_SOURCE_DIR}' to '{mod_dir}'")
    __configure(mod_dir)
    mod_entry_point = mod_dir.joinpath(MOD_ENTRY_POINT)
    patchers.patch_lua(mod_entry_point)


def __configure(mod_dir: Path) -> None:
    mod_config_file = mod_dir.joinpath(MOD_CONFIG_FILE)
    source_text = mod_config_file.read_text()
    (width, height) = config.new_viewport
    patched_text = WIDTH_REGEX.sub('\g<1>' + str(width), source_text)
    patched_text = HEIGHT_REGEX.sub('\g<1>' + str(height), patched_text)
    mod_config_file.write_text(patched_text)
    logger.info(f"Configured '{mod_config_file}' with viewport {config.new_viewport}")


def uninstall() -> None:
    mod_dir = config.hades_dir.joinpath(HADES_MOD_DIR)
    if mod_dir.exists():
        dir_util.remove_tree(str(mod_dir))
    logger.info(f"Uninstalled Lua mod from '{mod_dir}'")
