from collections import OrderedDict
from contextlib import contextmanager
import copy
from functools import partial, singledispatch
from pathlib import Path
import re
import struct
from typing import Any, Callable, Generator, Union

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


def __int_to_bytes(value: int) -> bytes:
    return struct.pack('<i', value)


def __float_to_bytes(value: float) -> bytes:
    return struct.pack('<f', value)


ENGINES = {
    'DirectX': 'x64/EngineWin64s.dll',
    'Vulkan': 'x64Vk/EngineWin64sv.dll',
    '32-bit': 'x86/EngineWin32s.dll',
}
HEX_PATCHES = {
    'width': {
        'regex': re.compile(rb'(\xc7\x05.{4})' + __int_to_bytes(config.DEFAULT_WIDTH)),
        'expected_subs': 2,
    },
    'height': {
        'regex': re.compile(rb'(\xc7\x05.{4})' + __int_to_bytes(config.DEFAULT_HEIGHT)),
        'expected_subs': 2,
    },
    'fullscreen_vector': {
        'regex': re.compile(__float_to_bytes(config.DEFAULT_WIDTH) + __float_to_bytes(config.DEFAULT_HEIGHT)),
    },
    'screencenter_vector': {
        'regex': re.compile(__float_to_bytes(config.DEFAULT_CENTER_X) + __float_to_bytes(config.DEFAULT_CENTER_Y)),
    },
}


def patch_engines() -> None:
    hex_patches = copy.deepcopy(HEX_PATCHES)
    hex_patches['width']['sub_with'] = b'\g<1>' + __int_to_bytes(config.new_width)
    hex_patches['height']['sub_with'] = b'\g<1>' + __int_to_bytes(config.new_height)
    hex_patches['fullscreen_vector']['sub_with'] = __float_to_bytes(config.new_width) + __float_to_bytes(config.new_height)
    hex_patches['screencenter_vector']['sub_with'] = __float_to_bytes(config.new_center_x) + __float_to_bytes(config.new_center_y)
    for engine, filepath in ENGINES.items():
        file = config.hades_dir.joinpath(filepath)
        LOGGER.debug(f"Patching {engine} backend at '{file}'")
        with safe_patch_file(file) as (original_file, file):
            __patch_engine(original_file, file, hex_patches)


def __patch_engine(original_file: Path, file: Path, hex_patches: dict[str, dict[str, Any]]
) -> None:
    data = original_file.read_bytes()
    for key, sub_dict in hex_patches.items():
        (data, sub_count) = sub_dict['regex'].subn(sub_dict['sub_with'], data)
        if 'expected_subs' in sub_dict and sub_count != sub_dict['expected_subs']:
             raise LookupError(f"'{key}' patching: expected {sub_dict['expected_subs']} matches in '{file}', found {sub_count}")
    file.write_bytes(data)
    LOGGER.info(f"Patched '{file}'")


def patch_engines_status() -> None:
    status = True
    for engine, filepath in ENGINES.items():
        file = config.hades_dir.joinpath(filepath)
        LOGGER.debug(f"Checking patch status of {engine} backend at '{file}'")
        data = file.read_bytes()
        checks = []
        for key, sub_dict in HEX_PATCHES.items():
            if 'expected_subs' in sub_dict:
                count = len(sub_dict['regex'].findall(data))
                checks.append(count == sub_dict['expected_subs'])
        if all(checks):
            LOGGER.info(f"Found default width/height values for {engine} backend at '{file}'")
            status = False
        else:
            LOGGER.info(f"Default width/height values not found for {engine} backend at '{file}'.")
    return status


SJSON_DIR = 'Content/Game'


def __update_children(children_dict: dict, data: OrderedDict) -> OrderedDict:
    patched = copy.deepcopy(data)
    for child_key, callback in children_dict.items():
        try:
            child_value = copy.deepcopy(patched[child_key])
            patched[child_key] = callback(patched[child_key])
            LOGGER.debug(f"Updated child '{child_key}' from '{child_value}' to '{patched[child_key]}'")
        except KeyError:
            raise KeyError(f"Did not find '{child_key}'.")
    return patched


def __upsert_siblings(lookup_key: str, lookup_value: str, sibling_dict: dict, data: OrderedDict) -> OrderedDict:
    try:
        if data[lookup_key] == lookup_value:
            patched = copy.deepcopy(data)
            for sibling_key, (callback, default) in sibling_dict.items():
                try:
                    sibling_value = copy.deepcopy(patched[sibling_key])
                    patched[sibling_key] = callback(patched[sibling_key])
                    LOGGER.debug(f"Found '{lookup_key} = {lookup_value}', updated sibling '{sibling_key}' from '{sibling_value}' to '{patched[sibling_key]}'")
                except KeyError:
                    if default:
                        patched[sibling_key] = callback(default)
                        LOGGER.debug(f"Found '{lookup_key} = {lookup_value}', inserted sibling '{sibling_key} = {patched[sibling_key]}'")
            return patched
        return data
    except KeyError:
        return data


def __add_offset(data: OrderedDict, scale: float=1.0) -> OrderedDict:
    # if element is scaled up/down, offset needs to adjusted accordingly
    multiplier = 1.0 / data.get('Scale', scale)
    offsetX = (config.new_center_x - config.DEFAULT_CENTER_X) * multiplier
    data['OffsetX'] = data.get('OffsetX', 0) + offsetX
    offsetY = (config.new_height - config.DEFAULT_HEIGHT) * multiplier
    data['OffsetY'] = data.get('OffsetY', 0) + offsetY
    return data


RECENTER = { 'X': helpers.recompute_fixed_X_from_center, 'Y': helpers.recompute_fixed_Y_from_center }
RECENTER_X_FIXED_BOTTOM = { 'X': helpers.recompute_fixed_X_from_center, 'Y': helpers.recompute_fixed_Y_from_bottom }
REPOSITION_X_FROM_LEFT_FIXED_TOP = { 'X': helpers.recompute_fixed_X_from_left }
REPOSITION_X_FROM_RIGHT_FIXED_TOP = { 'X': helpers.recompute_fixed_X_from_right }
RESIZE = { 'Width': partial(helpers.recompute_fixed_X_from_right, center_hud=False), 'Height': helpers.recompute_fixed_Y_from_bottom }
RESCALE = { 'ScaleX': (helpers.rescale_X, 1), 'ScaleY': (helpers.rescale_Y, 1) }
OFFSET_THING_SCALE_05 = { 'Thing': (partial(__add_offset, scale=0.5), OrderedDict()) }
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
                partial(__upsert_siblings, 'Name', 'FullscreenChaosDisplaceRings', { 'ScaleX': (helpers.rescale, 1), 'ScaleY': (helpers.rescale, 1) }),
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

                # Vignette displayed on low health
                partial(__upsert_siblings, 'Name', 'LowHealthShroud', RESCALE),

                # Room transitions
                partial(__upsert_siblings, 'Name', 'RoomTransitionIn', RESCALE),
                partial(__upsert_siblings, 'Name', 'RoomTransitionInBoatRide', RESCALE),
                partial(__upsert_siblings, 'Name', 'RoomTransitionOutBoatRide', RESCALE),

                # Dialogue backgrounds
                partial(__upsert_siblings, 'Name', 'DialogueBackgroundIn', RESCALE),

                # Main vignette overlay
                partial(__upsert_siblings, 'Name', 'VignetteOverlay', RESCALE),
            ],
        },
    },
    'GUI': {
        'AboutScreen.sjson': {
            'AboutScreen': {
                'Back': partial(__update_children, RESIZE),
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
                'Back': partial(__update_children, RESIZE),
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
                'Back': partial(__update_children, RESIZE),
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'ConnectSteamButton': partial(__update_children, RECENTER),
                'CancelButton': partial(__update_children, RECENTER),
                'DescriptionBox': partial(__update_children, RECENTER),
            },
        },
        'CloudSyncDialog.sjson': {
            'CloudSyncDialog': {
                'Back': partial(__update_children, RESIZE),
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
                'Back': partial(__update_children, RESIZE),
                'DebugKeyButton': partial(__update_children, REPOSITION_X_FROM_LEFT_FIXED_TOP),
                'LeftArrow': partial(__update_children, RECENTER),
                'FileFilter': partial(__update_children, REPOSITION_X_FROM_LEFT_FIXED_TOP),
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
                'UseText': partial(__update_children, RESIZE),
                'SubtitlesABacking': partial(__update_children, RECENTER_X_FIXED_BOTTOM),
                'SubtitlesBBacking': partial(__update_children, RECENTER_X_FIXED_BOTTOM),
                'BuildNumberText': partial(__update_children, REPOSITION_X_FROM_RIGHT_FIXED_TOP),
                'ElapsedRunTimeText': partial(__update_children, REPOSITION_X_FROM_RIGHT_FIXED_TOP),
                'ElapsedBiomeTimeText': partial(__update_children, { 'X': helpers.recompute_fixed_X_from_left, 'Y': helpers.recompute_fixed_Y_from_bottom }),
                'ActiveShrinePointText': partial(__update_children, REPOSITION_X_FROM_LEFT_FIXED_TOP),
                'SaveAnim': partial(__update_children, REPOSITION_X_FROM_RIGHT_FIXED_TOP),
            },
        },
        'KeyMappingScreen.sjson': {
            'KeyMappingScreen': {
                'Back': partial(__update_children, RESIZE),
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
                'Back': partial(__update_children, RESIZE),
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
                'Back': partial(__update_children, RESIZE),
                'MapButton': partial(__update_children, REPOSITION_X_FROM_LEFT_FIXED_TOP),
                'LeftArrow': partial(__update_children, RECENTER),
                'FileFilter': partial(__update_children, REPOSITION_X_FROM_LEFT_FIXED_TOP),
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
                'Back': partial(__update_children, RESIZE),
                'SaveFileButton': partial(__update_children, REPOSITION_X_FROM_LEFT_FIXED_TOP),
                'CancelButton': partial(__update_children, RECENTER),
                'LeftArrow': partial(__update_children, RECENTER),
                'FileFilter': partial(__update_children, REPOSITION_X_FROM_LEFT_FIXED_TOP),
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
                'Front': partial(__update_children, RESIZE),
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
                'Back': partial(__update_children, RESIZE),
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'MessageText': partial(__update_children, RECENTER),
                'TextBackground': partial(__update_children, RECENTER),
                'ConfirmButton': partial(__update_children, RECENTER),
            },
        },
        'MessageDialogLarge.sjson': {
            'MessageDialogLarge': {
                'Back': partial(__update_children, RESIZE),
                'AnimatedBackground': partial(__update_children, RECENTER),
                'TitleText': partial(__update_children, RECENTER),
                'MessageText': partial(__update_children, RECENTER),
                'TextBackground': partial(__update_children, RECENTER),
                'ConfirmButton': partial(__update_children, RECENTER),
            },
        },
        'MiscSettingsScreen.sjson': {
            'MiscSettingsScreen': {
                'Back': partial(__update_children, RESIZE),
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
                'Back': partial(__update_children, RESIZE),
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
                'Back': partial(__update_children, RESIZE),
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
                'Back': partial(__update_children, RESIZE),
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
                'Back': partial(__update_children, RESIZE),
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
                'Back': partial(__update_children, RESIZE),
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
                'CancelButton': partial(__update_children, { 'X': helpers.recompute_fixed_X_from_center }),
                'XButton': partial(__update_children, RECENTER),
            },
        },
        'ThreeWayDialog.sjson': {
            'ThreeWayDialog': {
                'Back': partial(__update_children, RESIZE),
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
    'Obstacles': {
        'GUI.sjson': {
            'Obstacles': [
                # Trait UI bottom decor
                partial(__upsert_siblings, 'Name', 'TraitTrayDecor_Artemis', OFFSET_THING_SCALE_05),
                partial(__upsert_siblings, 'Name', 'TraitTrayDecor_Chaos', OFFSET_THING_SCALE_05),
                partial(__upsert_siblings, 'Name', 'TraitTrayDecor_Music', OFFSET_THING_SCALE_05),
                partial(__upsert_siblings, 'Name', 'TraitTrayDecor_Hades', OFFSET_THING_SCALE_05),
                partial(__upsert_siblings, 'Name', 'TraitTrayDecor_Chthonic', OFFSET_THING_SCALE_05),
                partial(__upsert_siblings, 'Name', 'TraitTrayDecor_Blood', OFFSET_THING_SCALE_05),
                partial(__upsert_siblings, 'Name', 'TraitTrayDecor_Heat', OFFSET_THING_SCALE_05),
                partial(__upsert_siblings, 'Name', 'TraitTrayDecor_Stone', OFFSET_THING_SCALE_05),
                partial(__upsert_siblings, 'Name', 'TraitTrayDecor_Love', OFFSET_THING_SCALE_05),
            ],
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


def patch_lua(lua_scripts_dir: Path, import_statement: str) -> None:
    hook_file = lua_scripts_dir.joinpath(HOOK_FILE)
    LOGGER.debug(f"Patching Lua hook file at '{hook_file}'")
    with safe_patch_file(hook_file) as (original_file, file):
        __patch_hook_file(original_file, file, import_statement)


def __patch_hook_file(original_file: Path, file: Path, import_statement: str) -> None:
    source_text = original_file.read_text()
    source_text += f"""

-- Hephaistos hook
{import_statement}
"""
    file.write_text(source_text)
    LOGGER.info(f"Patched '{file}' with hook '{import_statement}'")


def patch_lua_status(lua_scripts_dir: Path, import_statement: str) -> None:
    hook_file = lua_scripts_dir.joinpath(HOOK_FILE)
    LOGGER.debug(f"Checking patch status of Lua hook file at '{hook_file}'")
    text = hook_file.read_text()
    if import_statement in text:
        LOGGER.info(f"Found hook '{import_statement}' in '{hook_file}'")
        return True
    else:
        LOGGER.info(f"No hook '{import_statement}' found in '{hook_file}'")
        return False
