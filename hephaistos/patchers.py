from collections import OrderedDict
from contextlib import contextmanager
import copy
from functools import partial, singledispatch
from pathlib import Path
import re
from typing import Callable, Generator, Pattern, Tuple, Union

import sjson

from hephaistos import backups, config, hashes, helpers, sjson_data
from hephaistos.config import LOGGER
from hephaistos.helpers import SJSON


SJSON_SUFFIX = '.sjson'


@contextmanager
def safe_patch_file(file: Path) -> Generator[Union[SJSON, Path], None, None]:
    """Context manager for patching files in a safe manner, wrapped by backup
    and hash handling.

    On first run:
    - Store a backup copy of the original file for restoration with the `restore` subcommand.
    - (If patching SJSON) Store a copy of the parsed SJSON data for speeding up subsequent patches.
    - Store patched hash in a text file.

    On subsequent runs, check current hash against previously stored hash:
    - If matching, repatch from the backup copy or stored SJSON data (if patching SJSON).
    - It not matching, the file has changed since the last patch.
    """
    if hashes.check(file):
        LOGGER.debug(f"Hash match for '{file}' -- repatching based on backup file")
        original_file = backups.get(file)
        if file.suffix == SJSON_SUFFIX:
            source_sjson = sjson_data.get(file)
    else:
        LOGGER.debug(f"No hash stored for '{file}' -- storing backup file")
        original_file = backups.store(file)
        if file.suffix == SJSON_SUFFIX:
            source_sjson = sjson_data.store(file)
    if file.suffix == SJSON_SUFFIX:
        yield (source_sjson, file)
    else:
        yield (original_file, file)
    hashes.store(file)


ENGINES = {
    'DirectX': 'x64/EngineWin64s.dll',
    'Vulkan': 'x64Vk/EngineWin64sv.dll',
    '32-bit': 'x86/EngineWin32s.dll',
}
BYTE_LENGTH = 4
BYTE_ORDER = 'little'
EXPECTED_SUBS = 2


def patch_engines() -> None:
    (current_width, current_height) = config.DEFAULT_VIRTUAL_VIEWPORT
    width_regex = re.compile(rb'(\xc7\x05.{4})' + __int_to_bytes(current_width))
    height_regex = re.compile(rb'(\xc7\x05.{4})' + __int_to_bytes(current_height))
    regexes = (width_regex, height_regex)

    for engine, filepath in ENGINES.items():
        file = config.hades_dir.joinpath(filepath)
        LOGGER.debug(f"Patching {engine} backend at '{file}'")
        with safe_patch_file(file) as (original_file, file):
            __patch_engine(original_file, file, regexes)


def __int_to_bytes(value: int) -> bytes:
    return value.to_bytes(BYTE_LENGTH, BYTE_ORDER)


def __patch_engine(original_file: Path, file: Path, regexes: Tuple[Pattern[bytes], Pattern[bytes]]
) -> None:
    source_bytes = original_file.read_bytes()
    (hex_width, hex_height) = [__int_to_bytes(value) for value in config.new_viewport]
    (patched_bytes, width_sub_count) = regexes[0].subn(b'\g<1>' + hex_width, source_bytes)
    (patched_bytes, height_sub_count) = regexes[1].subn(b'\g<1>' + hex_height, patched_bytes)

    if width_sub_count != EXPECTED_SUBS or height_sub_count != EXPECTED_SUBS:
        raise LookupError(f"Expected {EXPECTED_SUBS} matches in '{file}', found {width_sub_count} for width and {height_sub_count} for height")
    file.write_bytes(patched_bytes)
    LOGGER.info(f"Patched '{file}'")


SJSON_DIR = 'Content/Game'


def __update_children(children_dict: dict, data: OrderedDict) -> OrderedDict:
    try:
        patched = copy.deepcopy(data)
        for child_key, callback in children_dict.items():
            child_value = patched[child_key]
            patched[child_key] = callback(child_value)
            LOGGER.debug(f"Updated child '{child_key}' from '{child_value}' to '{patched[child_key]}'")
        return patched
    except KeyError:
        return data


def __upsert_siblings(lookup_key: str, lookup_value: str, sibling_dict: dict, data: OrderedDict) -> OrderedDict:
    try:
        if data[lookup_key] == lookup_value:
            patched = copy.deepcopy(data)
            for sibling_key, (callback, default) in sibling_dict.items():
                try:
                    sibling_value = patched[sibling_key]
                    patched[sibling_key] = callback(sibling_value)
                    LOGGER.debug(f"Found '{lookup_key} = {lookup_value}', updated sibling '{sibling_key}' from '{sibling_value}' to '{patched[sibling_key]}'")
                except KeyError:
                    if default:
                        patched[sibling_key] = callback(default)
                        LOGGER.debug(f"Found '{lookup_key} = {lookup_value}', inserted sibling '{sibling_key} = {patched[sibling_key]}'")
            return patched
        return data
    except KeyError:
        return data

RECENTER = { 'X': helpers.recompute_fixed_X, 'Y': helpers.recompute_fixed_Y }
RESIZE = { 'Width': helpers.recompute_fixed_X, 'Height': helpers.recompute_fixed_Y }
RESCALE = { 'ScaleX': (helpers.rescale_X, 1), 'ScaleY': (helpers.rescale_Y, 1) }
RESCALE_MAX = { 'ScaleX': (helpers.rescale, 1), 'ScaleY': (helpers.rescale, 1) }
SJON_PATCHES = {
    'Animations': {
        'Fx.sjson': {
            'Animations': [
                # Vignettes displayed when hit by lava / poison / [Redacted] boiling blood
                partial(__upsert_siblings, 'Name', 'LavaVignetteA', RESCALE),
                partial(__upsert_siblings, 'Name', 'PoisonVignetteLoop', RESCALE),
                partial(__upsert_siblings, 'Name', 'HadesBloodstoneVignette', RESCALE),

                # Fullscreen displacement overlays FX
                partial(__upsert_siblings, 'Name', 'FullscreenAlertDisplace', RESCALE),
                partial(__upsert_siblings, 'Name', 'BoonInteractDisplace', RESCALE),
                partial(__upsert_siblings, 'Name', 'FullscreenChaosDisplace', RESCALE),
                partial(__upsert_siblings, 'Name', 'FullscreenChaosDisplaceRings', RESCALE_MAX),
                partial(__upsert_siblings, 'Name', 'FullscreenAlertColor', RESCALE),
                partial(__upsert_siblings, 'Name', 'FullscreenAlertColorDark', RESCALE),
                partial(__upsert_siblings, 'Name', 'FullscreenAlertColorInvert', RESCALE),
                partial(__upsert_siblings, 'Name', 'LegendaryAspectSnow', RESCALE),
                partial(__upsert_siblings, 'Name', 'WeaponKitProphecyStreaks', RESCALE),
                partial(__upsert_siblings, 'Name', 'WeaponKitInteractVignette', RESCALE),
                partial(__upsert_siblings, 'Name', 'WeaponKitInteractVignetteOverlay', RESCALE),

                # Assist / summon overlays
                partial(__upsert_siblings, 'Name', 'WrathPresentationStreak', RESCALE),
                partial(__upsert_siblings, 'Name', 'WrathPresentationBottomDivider', RESCALE),
                partial(__upsert_siblings, 'Name', 'WrathVignette', RESCALE),
            ],
        },
        'GUIAnimations.sjson': {
            'Animations': [
                # Vignette displayed when hit
                partial(__upsert_siblings, 'Name', 'BloodFrame', RESCALE),
            ],
        },
    },
    'GUI': {
        'AboutScreen.sjson': {
            'AboutScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'UpArrow': partial(__update_children, RECENTER),
                'DownArrow': partial(__update_children, RECENTER),
                'CreditText': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'AnnouncementScreen.sjson': {
            'AnnouncementScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'SubHeader': partial(__update_children, RECENTER),
                'UpArrow': partial(__update_children, RECENTER),
                'DownArrow': partial(__update_children, RECENTER),
                'AnnouncementText': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'CloudSaveUploadDialog.sjson': {
            'CloudSaveUploadDialog': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'MessageText': partial(__update_children, RECENTER),
                'TextBackground': partial(__update_children, RECENTER),
                'ConfirmButton': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'CloudSettingsScreen.sjson': {
            'CloudSettingsScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'ConnectSteamButton': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
                'DescriptionBox': partial(__update_children, RECENTER),
            },
        },
        'CloudSyncDialog.sjson': {
            'CloudSyncDialog': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'MessageText': partial(__update_children, RECENTER),
                'TextBackground': partial(__update_children, RECENTER),
                'ConfirmButton': partial(__update_children, RECENTER),
            },
        },
        'DebugDrawGroupScreen.sjson': {
            'DebugDrawGroupScreen': {
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'DebugKeyScreen.sjson': {
            'DebugKeyScreen': {
                'DebugKeyButton': partial(__update_children, RECENTER),
                'LeftArrow': partial(__update_children, RECENTER),
                'FileFilter': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'DownloadScreen.sjson': {
            'DownloadScreen': {
                'Character': partial(__update_children, RECENTER),
                'ProgressBar': partial(__update_children, RECENTER),
                'ProgressText': partial(__update_children, RECENTER),
            },
        },
        'ExitConfirmDialog.sjson': {
            'ExitConfirmDialog': {
                'Back': partial(__update_children, RESIZE),
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'PromptText': partial(__update_children, RECENTER),
                'TextBackground': partial(__update_children, RECENTER),
                'ConfirmButton': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'InGameUI.sjson': {
            'InGameUI': {
                'SubtitlesABacking': partial(__update_children, RECENTER),
                'SubtitlesBBacking': partial(__update_children, RECENTER),
                'BuildNumberText': partial(__update_children, RECENTER),
                'ElapsedRunTimeText': partial(__update_children, RECENTER),
                'ElapsedBiomeTimeText': partial(__update_children, RECENTER),
                'ActiveShrinePointText': partial(__update_children, RECENTER),
                'SaveAnim': partial(__update_children, RECENTER),
            },
        },
        'KeyMappingScreen.sjson': {
            'KeyMappingScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'AnimatedBackgroundTop': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'ControlLabel': partial(__update_children, RECENTER),
                'InfoPanel': partial(__update_children, RECENTER),
                'InfoText': partial(__update_children, RECENTER),
                'DefaultsButton': partial(__update_children, RECENTER),
                'RemapInstructions': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'LanguageScreen.sjson': {
            'LanguageScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'LanguageButton': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'LaunchScreen.sjson': {
            'LaunchScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'ProgressBar': partial(__update_children, RECENTER),
                'WorkText': partial(__update_children, RECENTER),
                'DebugHintText': partial(__update_children, RECENTER),
            },
        },
        'LoadMapScreen.sjson': {
            'LoadMapScreen': {
                'MapButton': partial(__update_children, RECENTER),
                'LeftArrow': partial(__update_children, RECENTER),
                'FileFilter': partial(__update_children, RECENTER),
                'AlphabeticalSortButton': partial(__update_children, RECENTER),
                'ChronologicalSortButton': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'LoadReplayScreen.sjson': {
            'LoadReplayScreen': {
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'LoadSaveScreen.sjson': {
            'LoadSaveScreen': {
                'SaveFileButton': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
                'FileFilter': partial(__update_children, RECENTER),
                'AlphabeticalSortButton': partial(__update_children, RECENTER),
                'ChronologicalSortButton': partial(__update_children, RECENTER),
                'LoadSpinner': partial(__update_children, RECENTER),
                'NotableSaveInfo': partial(__update_children, RECENTER),
                'RareFormat': partial(__update_children, RECENTER),
            },
        },
        'LoadScreen.sjson': {
            'LoadScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'ProgressBar': partial(__update_children, RECENTER),
            },
        },
        'MainMenuScreen.sjson': {
            'MainMenuScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'Logo': partial(__update_children, RECENTER),
                'Character': partial(__update_children, RECENTER),
                'UpdateTitleBacking': partial(__update_children, RECENTER),
                'FullScreenFade': partial(__update_children, RECENTER),
                'PlayGameButton': partial(__update_children, RECENTER),
                'NextUpdateButton': partial(__update_children, RECENTER),
                'UpdateTitleText': partial(__update_children, RECENTER),
                'FeedbackButton': partial(__update_children, RECENTER),
            },
        },
        'MenuScreen.sjson': {
            'MenuScreen': {
                'InfoPanel': partial(__update_children, RECENTER),
            },
        },
        'MessageDialog.sjson': {
            'MessageDialog': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'MessageText': partial(__update_children, RECENTER),
                'TextBackground': partial(__update_children, RECENTER),
                'ConfirmButton': partial(__update_children, RECENTER),
            },
        },
        'MessageDialogLarge.sjson': {
            'MessageDialogLarge': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'MessageText': partial(__update_children, RECENTER),
                'TextBackground': partial(__update_children, RECENTER),
                'ConfirmButton': partial(__update_children, RECENTER),
            },
        },
        'MiscSettingsScreen.sjson': {
            'MiscSettingsScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'BrightnessLabel': partial(__update_children, RECENTER),
                'BrightnessSlider': partial(__update_children, RECENTER),
                'MasterLabel': partial(__update_children, RECENTER),
                'MasterSlider': partial(__update_children, RECENTER),
                'DescriptionBox': partial(__update_children, RECENTER),
                'InfoPanel': partial(__update_children, RECENTER),
                'InfoText': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
                'XButton': partial(__update_children, RECENTER),
            },
        },
        'PatchNotesScreen.sjson': {
            'PatchNotesScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'SubHeader': partial(__update_children, RECENTER),
                'ScrollBar': partial(__update_children, RECENTER),
                'ScrollBarTracker': partial(__update_children, RECENTER),
                'UpArrow': partial(__update_children, RECENTER),
                'DownArrow': partial(__update_children, RECENTER),
                'AnnouncementText': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'PauseScreen.sjson': {
            'PauseScreen': {
                'Back': partial(__update_children, RESIZE),
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'ResumeGameButton': partial(__update_children, RECENTER),
                'LastSaveTimeHint': partial(__update_children, RECENTER),
            },
        },
        'ProfileScreen.sjson': {
            'ProfileScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'FullScreenFade': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'ContinueGameButton': partial(__update_children, RECENTER),
                'SaveSpinnerHint': partial(__update_children, RECENTER),
                'InstructionHint': partial(__update_children, RECENTER),
                'ProfileButton': partial(__update_children, RECENTER),
                'HardModeButton': partial(__update_children, RECENTER),
                'DeleteButton': partial(__update_children, RECENTER),
                'InfoPanel': partial(__update_children, RECENTER),
                'InfoText': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'RemoteProfileScreen.sjson': {
            'RemoteProfileScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'FullScreenFade': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'ContinueGameButton': partial(__update_children, RECENTER),
                'SaveSpinnerHint': partial(__update_children, RECENTER),
                'InstructionHint': partial(__update_children, RECENTER),
                'ProfileButton': partial(__update_children, RECENTER),
                'HardModeButton': partial(__update_children, RECENTER),
                'DeleteButton': partial(__update_children, RECENTER),
                'InfoPanel': partial(__update_children, RECENTER),
                'InfoText': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'ResolutionScreen.sjson': {
            'ResolutionScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'ResolutionButton': partial(__update_children, RECENTER),
                'ConfirmButton': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'SettingsMenuScreen.sjson': {
            'SettingsMenuScreen': {
                'Back': partial(__update_children, RESIZE),
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'SettingsButton': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'StartNewGameScreen.sjson': {
            'StartNewGameScreen': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'FullScreenFade': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'StartNewGameHint': partial(__update_children, RECENTER),
                'ConfirmButton': partial(__update_children, RECENTER),
                'SubtitlesButton': partial(__update_children, RECENTER),
                'DescriptionBox': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
        'SVNLockDialog.sjson': {
            'SVNLockDialog': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'PromptText': partial(__update_children, RECENTER),
                'TextBackground': partial(__update_children, RECENTER),
                'ConfirmButton': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
                'XButton': partial(__update_children, RECENTER),
            },
        },
        'ThreeWayDialog.sjson': {
            'ThreeWayDialog': {
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'PromptText': partial(__update_children, RECENTER),
                'TextBackground': partial(__update_children, RECENTER),
                'ConfirmButton': partial(__update_children, RECENTER),
                'ConfirmAlternateButton': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
            },
        },
    },
}


def patch_sjsons() -> None:
    sjson_dir = config.hades_dir.joinpath(SJSON_DIR)
    for dirname, files in SJON_PATCHES.items():
        sub_dir = sjson_dir.joinpath(dirname)
        for filename, patches in files.items():
            file = sub_dir.joinpath(filename)
            LOGGER.debug(f"Patching SJSON file at '{file}'")
            with safe_patch_file(file) as (source_sjson, file):
                __patch_sjson_file(source_sjson, file, patches)


def __patch_sjson_file(source_sjson: SJSON, file: Path, patches: dict) -> None:
    patched_sjson = __patch_sjson_data(source_sjson, patches)
    file.write_text(sjson.dumps(patched_sjson))
    LOGGER.info(f"Patched '{file}'")


@singledispatch
def __patch_sjson_data(data: OrderedDict, patch: Union[dict, Callable], previous_path: str=None) -> SJSON:
    patched = copy.deepcopy(data)
    if isinstance(patch, dict):
        for key, patches in patch.items():
            current_path = key if previous_path is None else f'{previous_path}.{key}'
            patched[key] = __patch_sjson_data(patched[key], patches, current_path)
    else:
        LOGGER.debug(f"Patching '{previous_path}'")
        patched = patch(data=patched)
    return patched


@__patch_sjson_data.register
def _(data: list, patches: list, previous_path: str=None) -> SJSON:
    patched = copy.deepcopy(data)
    current_path = '[]' if previous_path is None else f'{previous_path}.[]'
    LOGGER.debug(f"Patching '{current_path}'")
    for patch in patches:
        patched = [patch(data=item) for item in patched]
    return patched


HOOK_FILE = 'RoomManager.lua'


def patch_lua(lua_scripts_dir: Path, relative_path_to_mod_entry_point: str) -> None:
    hook_file = lua_scripts_dir.joinpath(HOOK_FILE)
    LOGGER.debug(f"Patching Lua hook file at '{hook_file}'")
    with safe_patch_file(hook_file) as (original_file, file):
        __patch_hook_file(original_file, file, relative_path_to_mod_entry_point)


def __patch_hook_file(original_file: Path, file: Path, relative_path_to_mod_entry_point: str) -> None:
    statement = f'Import "{relative_path_to_mod_entry_point}"'
    source_text = original_file.read_text()
    source_text += f"""

-- Hephaistos hook
{statement}
"""
    file.write_text(source_text)
    LOGGER.info(f"Patched '{file}' with hook '{statement}'")
