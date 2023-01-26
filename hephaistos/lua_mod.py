from distutils import dir_util
import os.path
from pathlib import Path
import re

from hephaistos import config, helpers, patchers
from hephaistos.config import LOGGER


MOD_TARGET_DIR = 'Mods/Hephaistos'
LUA_SCRIPTS_DIR = 'Scripts'
MOD_ENTRY_POINT = 'Hephaistos.lua'
MOD_CONFIG_FILE = 'HephaistosConfig.lua'
WIDTH_REGEX = re.compile(r'(Hephaistos.ScreenWidth = )\d+')
HEIGHT_REGEX = re.compile(r'(Hephaistos.ScreenHeight = )\d+')
CENTER_HUD_REGEX = re.compile(r'(Hephaistos.CenterHUD = ).+')
IMPORT_REGEX = re.compile(r'Import "../Mods/Hephaistos/(.*)"')


def install() -> None:
    LOGGER.debug(f"Installing Lua mod from '{config.MOD_SOURCE_DIR}'")
    (mod_dir, lua_scripts_dir, relative_path_to_mod, import_statement) = __prepare_variables()
    dir_util.copy_tree(str(config.MOD_SOURCE_DIR), str(mod_dir))
    LOGGER.debug(f"Copied '{config.MOD_SOURCE_DIR}' to '{mod_dir}'")
    __configure(mod_dir, relative_path_to_mod)
    LOGGER.info(f"Installed Lua mod to '{mod_dir}'")
    # run modimporter (if available) to register Hephaistos
    if config.modimporter:
        LOGGER.info(f"Running 'modimporter' to register Hephaistos")
        helpers.run_modimporter()
    # otherwise register manually
    else:
        patchers.patch_lua(lua_scripts_dir, import_statement)


def __prepare_variables() -> tuple[Path, Path, str]:
    # copy mod files
    mod_dir = config.content_dir.joinpath(MOD_TARGET_DIR)
    mod_dir.mkdir(parents=True, exist_ok=True)

    # compute relative path from Hades scripts dir to mod
    lua_scripts_dir = config.content_dir.joinpath(LUA_SCRIPTS_DIR)
    relative_path_to_mod = os.path.relpath(mod_dir, lua_scripts_dir)
    # replace backward slashes with forward slashes on Windows and add trailing slash
    relative_path_to_mod = relative_path_to_mod.replace('\\', '/') + '/'
    LOGGER.debug(f"Computed relative path '{relative_path_to_mod}' from '{lua_scripts_dir}' to '{mod_dir}'")
    import_statement = f'Import "{relative_path_to_mod + MOD_ENTRY_POINT}"'
    return (mod_dir, lua_scripts_dir, relative_path_to_mod, import_statement)


def __configure(mod_dir: Path, relative_path_to_mod: str) -> None:
    # configure viewport
    mod_config_file = mod_dir.joinpath(MOD_CONFIG_FILE)
    source_text = mod_config_file.read_text()
    patched_text = WIDTH_REGEX.sub('\g<1>' + str(config.new_screen.width), source_text)
    patched_text = HEIGHT_REGEX.sub('\g<1>' + str(config.new_screen.height), patched_text)
    patched_text = CENTER_HUD_REGEX.sub('\g<1>' + str(config.center_hud).lower(), patched_text)
    mod_config_file.write_text(patched_text)
    LOGGER.debug(f"Configured '{mod_config_file}'")

    # configure internal mod imports
    for file in mod_dir.glob('**/*.lua'):
        source_text = file.read_text()
        (patched_text, count) = IMPORT_REGEX.subn(f'Import "{relative_path_to_mod}\g<1>"', source_text)
        if count:
            file.write_text(patched_text)
            LOGGER.debug(f"Configured '{file}' internal mod imports ({count} occurrences)")


def uninstall() -> None:
    mod_dir = config.content_dir.joinpath(MOD_TARGET_DIR)
    if mod_dir.exists():
        dir_util.remove_tree(str(mod_dir))
        LOGGER.info(f"Uninstalled Lua mod from '{mod_dir}'")
    else:
        LOGGER.info(f"No Lua mod to uninstall from '{mod_dir}'")


def status() -> None:
    mod_dir = config.content_dir.joinpath(MOD_TARGET_DIR)
    if mod_dir.exists() and any(mod_dir.iterdir()):
        LOGGER.info(f"Found Lua mod at '{mod_dir}'")
        (mod_dir, lua_scripts_dir, relative_path_to_mod, _) = __prepare_variables()
        return patchers.patch_lua_status(lua_scripts_dir, relative_path_to_mod + MOD_ENTRY_POINT)
    else:
        LOGGER.info(f"No Lua mod found at '{mod_dir}'")
        return False
