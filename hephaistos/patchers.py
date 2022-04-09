import contextlib
import copy
from enum import Enum
from functools import partial, singledispatch
from pathlib import Path
import re
import struct
from typing import Any, Callable, Generator, Tuple, TypedDict, Union

import sjson

from hephaistos import backups, config, hashes, helpers
from hephaistos.config import LOGGER
from hephaistos.helpers import IntOrFloat, Platform


SJSON = Union[dict, list, str, IntOrFloat, Any]


@contextlib.contextmanager
def safe_patch_file(file: Path, store_backup: bool=True) -> Generator[Tuple[Union[SJSON, Path], Path], None, None]:
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
    try:
        if hashes.check(file):
            LOGGER.debug(f"Hash match for '{file}': repatching based on backup file")
            original_file, source_sjson = backups.get(file)
        elif store_backup:
            LOGGER.debug(f"No hash stored for '{file}': storing backup file")
            original_file, source_sjson = backups.store(file)
        else:
            LOGGER.debug(f"No hash stored for '{file}'")
            original_file, source_sjson = None, None
    except hashes.HashMismatch as e:
        if config.force: # if using '--force', discard existing backup / hash and use new file as basis
            LOGGER.debug(f"Hash mismatch for '{file}' but running with '--force': patching based on new file")
            original_file, source_sjson = backups.store(file)
        else: # otherwise let caller decide what to do
            raise e
    if file.suffix == config.SJSON_SUFFIX:
        yield (source_sjson, file)
    else:
        yield (original_file, file)
    if store_backup:
        hashes.store(file)


class Engine(str, Enum):
    DIRECTX64 = 'DirectX (64-bit)'
    VULKAN = 'Vulkan (64-bit)'
    DIRECTX32 = 'DirectX (32-bit)'
    DIRECTX64_MS_STORE = 'DirectX (64-bit / Microsoft Store)'
    METAL = 'Metal'


ENGINES = {
    Platform.WINDOWS: {
        Engine.DIRECTX64: 'x64/EngineWin64s.dll',
        Engine.VULKAN: 'x64Vk/EngineWin64sv.dll',
        Engine.DIRECTX32: 'x86/EngineWin32s.dll',
    },
    Platform.MS_STORE: {
        # Microsoft Store version ships with 64-bit DirectX, but it seems to
        # have different imports and is thus compiled separately, resulting in
        # slight differences with the regular 64-bit DirectX version
        Engine.DIRECTX64_MS_STORE: 'Content/EngineWin64s.dll',
    },
    Platform.MACOS: {
        Engine.METAL: 'Game.macOS.app/Contents/MacOS/Game.macOS',
    },
}
# Steam on Linux uses Proton to wrap around the Windows version
ENGINES[Platform.LINUX] = ENGINES[Platform.WINDOWS]


class HexPatch(TypedDict, total=False):
    pattern: re.Pattern
    replacement: str
    replacement_args: tuple[bytes, ...]
    expected_subs: int


def __int_to_bytes(value: int) -> bytes:
    return struct.pack('<i', value)


def __float_to_bytes(value: float) -> bytes:
    return struct.pack('<f', value)


HEX_PATCHES: dict[str, HexPatch] = {
    # sgg::App::OnStart > override VIRTUAL_WIDTH and VIRTUAL_HEIGHT
    # fix viewport
    # sgg::Camera::Camera > override default width and height
    # fix camera extents / rendering
    'viewport': {
        'pattern': re.compile(rb'(\xc7.{5})' + __int_to_bytes(config.DEFAULT_SCREEN.width) + rb'(\xc7.{5})' + __int_to_bytes(config.DEFAULT_SCREEN.height)),
        'replacement': b'\g<1>%b\g<2>%b',
        'expected_subs': 2,
        Engine.METAL: {
            'pattern': re.compile(rb'(\x48\xb8.{4})?' +__int_to_bytes(config.DEFAULT_SCREEN.width) + rb'(.{14}\xc7\x05.{4})?' + __int_to_bytes(config.DEFAULT_SCREEN.height)),
        },
    },
    # sgg::LoadScreen::Draw > override Vector2 __xmm@4487000044f000000000000000000000
    # on x64, fix Styx -> [Redacted] load screen transition
    # sgg::GUIConstants::FULL_SCREEN > override Vector2
    # fix camera tether reference point calculations
    'fullscreen_vector': {
        'pattern': re.compile(__float_to_bytes(config.DEFAULT_SCREEN.width) + __float_to_bytes(config.DEFAULT_SCREEN.height)),
        'replacement': b'%b%b',
        'expected_subs': 245,
        # on x86, the Styx -> [Redacted] load screen transition is split over 2 floats and patched separately
        Engine.DIRECTX32: {
            'expected_subs': 244,
        },
        # on Microsoft Store, some more vector instances
        Engine.DIRECTX64_MS_STORE: {
            'expected_subs': 246,
        },
        # on MacOS, there are less vector instances
        Engine.METAL: {
            'expected_subs': 234,
        },
    },
    # sgg::InputHandler::SelectInDirection/SearchInDirection > override floats __real@44870000 and __real@44f00000
    # fix controller input selection not working when menus are repositioned outside of default viewport
    # sgg::LoadScreen::Draw
    # on x86, fix Styx -> [Redacted] load screen transition
    'width_height_floats': {
        'pattern': re.compile(__float_to_bytes(config.DEFAULT_SCREEN.height) + rb'(' + __float_to_bytes(1440) + __float_to_bytes(1632) + rb')' + __float_to_bytes(config.DEFAULT_SCREEN.width)),
        'replacement': b'%b\g<1>%b',
        'expected_subs': 1,
        Engine.DIRECTX32: {
            'pattern': re.compile(__float_to_bytes(config.DEFAULT_SCREEN.height) + rb'(' + __float_to_bytes(1250) + __float_to_bytes(1440) + __float_to_bytes(1600) + __float_to_bytes(1632) + rb')' + __float_to_bytes(config.DEFAULT_SCREEN.width)),
        },
        # on macOS, this is already handled by the `fullscreen_vector` patch
        Engine.METAL: {
            'expected_subs': 0,
        },
    },
    # sgg::GUIConstants::NATIVE_CENTER > override Vector2 
    # sgg::GUIConstants::SCREEN_CENTER > override Vector2
    # fix camera tether reference point calculations
    'screencenter_vector': {
        'pattern': re.compile(__float_to_bytes(config.DEFAULT_SCREEN.center_x) + __float_to_bytes(config.DEFAULT_SCREEN.center_y)),
        'replacement': b'%b%b',
        'expected_subs': 488,
        # on Microsoft Store, some more vector instances
        Engine.DIRECTX64_MS_STORE: {
            'expected_subs': 490,
        },
        # on MacOS, there are less vector instances and both NATIVE_CENTER and
        # SCREEN_CENTER are set at once from the same static value, hence the
        # number of replacements being approximately halved
        Engine.METAL: {
            'expected_subs': 230,
        },
    },
}


def __get_engine_specific_hex_patches(engine) -> None:
    hex_patches = copy.deepcopy(HEX_PATCHES)
    for _, hex_patch in hex_patches.items():
        # override engine-specific values if any
        engine_overrides = hex_patch.get(engine, {})
        for key, value in engine_overrides.items():
            hex_patch[key] = value
    return hex_patches


def patch_engines() -> None:
    HEX_PATCHES['viewport']['replacement_args'] = (__int_to_bytes(config.new_screen.width), __int_to_bytes(config.new_screen.height))
    HEX_PATCHES['fullscreen_vector']['replacement_args'] = (__float_to_bytes(config.new_screen.width), __float_to_bytes(config.new_screen.height))
    HEX_PATCHES['width_height_floats']['replacement_args'] = (__float_to_bytes(config.new_screen.height), __float_to_bytes(config.new_screen.width))
    HEX_PATCHES['screencenter_vector']['replacement_args'] = (__float_to_bytes(config.new_screen.center_x), __float_to_bytes(config.new_screen.center_y))
    for engine, filepath in ENGINES[config.platform].items():
        hex_patches = __get_engine_specific_hex_patches(engine)
        file = config.hades_dir.joinpath(filepath)
        LOGGER.debug(f"Patching '{engine}' backend at '{file}'")
        got_any_warnings = False
        with safe_patch_file(file) as (original_file, file):
            if not __patch_engine(original_file, file, engine, hex_patches):
                got_any_warnings = True
    if got_any_warnings:
        LOGGER.warning("Hephaistos managed to apply all hex patches but did not patch everything exactly as expected.")
        LOGGER.warning("This is most probably due to a game update.")
        LOGGER.warning("In most cases this is inconsequential and Hephaistos will work anyway, but Hephaistos might need further changes to work properly with the new version of the game.")


def __patch_engine(original_file: Path, file: Path, engine: str, hex_patches: dict[str, HexPatch]
) -> bool:
    """Return True if patch went as expected, False if any warnings happened."""
    data = original_file.read_bytes()
    all_as_expected = True
    for hex_patch_name, hex_patch in hex_patches.items():
        replacement = hex_patch['replacement'] % hex_patch['replacement_args']
        pattern = hex_patch['pattern']
        (data, sub_count) = pattern.subn(replacement, data)
        LOGGER.debug(f"Replaced {sub_count} occurrences of '{hex_patch_name}' pattern {pattern.pattern} with {replacement} in '{file}'")
        expected = hex_patch['expected_subs']
        if sub_count == 0 and expected != 0:
            raise LookupError(f"Failed to apply '{hex_patch_name}' patch in '{file}' (no occurrences found)")
        elif sub_count != expected:
            LOGGER.warning(f"Expected {expected} matches for '{hex_patch_name}' patch in '{file}', found {sub_count}")
            all_as_expected = False
    file.write_bytes(data)
    LOGGER.info(f"Patched '{file}'")
    return all_as_expected


def patch_engines_status() -> None:
    status = True
    for engine, filepath in ENGINES[config.platform].items():
        file = config.hades_dir.joinpath(filepath)
        LOGGER.debug(f"Checking patch status of '{engine}' backend at '{file}'")
        try:
            with safe_patch_file(file, store_backup=False) as (original_file, file):
                if original_file is not None:
                    LOGGER.info(f"'{file}' looks patched")
                else:
                    status = False
                    LOGGER.info(f"'{file}' is not patched")
        except hashes.HashMismatch:
            status = False
            LOGGER.info(f"'{file}' has been modified since last backup: probably not patched")
    return status


def __update_children(children_dict: dict, data: dict) -> dict:
    patched = copy.deepcopy(data)
    for child_key, callback in children_dict.items():
        try:
            child_value = copy.deepcopy(patched[child_key])
            patched[child_key] = callback(patched[child_key])
            LOGGER.debug(f"Updated child '{child_key}' from '{child_value}' to '{patched[child_key]}'")
        except KeyError:
            raise KeyError(f"Did not find '{child_key}'.")
    return patched


def __upsert_siblings(lookup_key: str, lookup_value: str, sibling_dict: dict, data: dict) -> dict:
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


def __add_offset(data: dict, scale: float=1.0) -> dict:
    # if element is scaled up/down, offset needs to adjusted accordingly
    multiplier = 1.0 / data.get('Scale', scale)
    offsetX = (config.new_screen.center_x - config.DEFAULT_SCREEN.center_x) * multiplier
    data['OffsetX'] = data.get('OffsetX', 0) + offsetX
    offsetY = (config.new_screen.height - config.DEFAULT_SCREEN.height) * multiplier
    data['OffsetY'] = data.get('OffsetY', 0) + offsetY
    return data


RECENTER = { 'X': helpers.recompute_fixed_X_from_center, 'Y': helpers.recompute_fixed_Y_from_center }
RECENTER_X_FIXED_BOTTOM = { 'X': helpers.recompute_fixed_X_from_center, 'Y': helpers.recompute_fixed_Y_from_bottom }
REPOSITION_X_FROM_LEFT_FIXED_TOP = { 'X': helpers.recompute_fixed_X_from_left }
REPOSITION_X_FROM_RIGHT_FIXED_TOP = { 'X': helpers.recompute_fixed_X_from_right }
RESIZE = { 'Width': partial(helpers.recompute_fixed_X_from_right, center_hud=False), 'Height': helpers.recompute_fixed_Y_from_bottom }
RESCALE = { 'ScaleX': (helpers.rescale_X, 1), 'ScaleY': (helpers.rescale_Y, 1) }
OFFSET_THING_SCALE_05 = { 'Thing': (partial(__add_offset, scale=0.5), {}) }
SJSONPatch = Union[dict[str, Callable], list[Callable]]
SJON_PATCHES: dict[str, dict[str, dict[str, SJSONPatch]]] = {
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
                partial(__upsert_siblings, 'Name', 'RoomTransitionInBlack', RESCALE),
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


SJSON_DIR = 'Game'


def patch_sjsons() -> None:
    LOGGER.info("Reading SJSON data (this operation can take time, please be patient)")
    sjson_dir = config.content_dir.joinpath(SJSON_DIR)
    for dirname, files in SJON_PATCHES.items():
        sub_dir = sjson_dir.joinpath(dirname)
        for filename, patches in files.items():
            file = sub_dir.joinpath(filename)
            LOGGER.debug(f"Patching SJSON file at '{file}'")
            with safe_patch_file(file) as (source_sjson, file):
                __patch_sjson_file(source_sjson, file, patches)


def __patch_sjson_file(source_sjson: SJSON, file: Path, patches: SJSONPatch) -> None:
    patched_sjson = __patch_sjson_data(source_sjson, patches)
    file.write_text(sjson.dumps(patched_sjson))
    LOGGER.info(f"Patched '{file}'")


@singledispatch
def __patch_sjson_data(data: dict, patch: Union[dict[str, SJSONPatch], Callable], previous_path: str=None) -> SJSON:
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
def _(data: list, patches: list[Callable], previous_path: str=None) -> SJSON:
    patched = copy.deepcopy(data)
    current_path = '[]' if previous_path is None else f'{previous_path}.[]'
    LOGGER.debug(f"Patching '{current_path}'")
    for patch in patches:
        patched = [patch(data=item) for item in patched]
    return patched


WINDOW_XY_DEFAULT_OFFSET = 100
WINDOW_XY_OVERFLOW_THRESHOLD = 32767


def patch_profile_sjsons() -> None:
    if config.custom_resolution:
        profile_sjsons = helpers.try_get_profile_sjson_files()
        if not profile_sjsons:
            msg = """Cannot patch custom resolution to 'ProfileX.sjson'.
This is a non-blocking issue but might prevent you from running Hades at the resolution of your choice."""
            LOGGER.warning(msg)
            return
        edited_list = []
        for file in profile_sjsons:
            LOGGER.debug(f"Analyzing '{file}'")
            data = sjson.loads(file.read_text())
            for key in ['X', 'WindowWidth']:
                data[key] = config.resolution.width
            for key in ['Y', 'WindowHeight']:
                data[key] = config.resolution.height
            # we manually set WindowX/Y in ProfileX.sjson configuration files as a
            # safeguard against WindowX/Y values overflowing when switching to
            # windowed mode while using a custom resolution larger than officially
            # supported by the main monitor, ensuring Hades will not be drawn
            # offscreen and can then be repositioned by the user
            for key in ['WindowX', 'WindowY']:
                if not key in data:
                    data[key] = WINDOW_XY_DEFAULT_OFFSET
                    LOGGER.debug(f"'{key}' not found in '{file.name}', inserted '{key} = {WINDOW_XY_DEFAULT_OFFSET}'")
                elif data[key] >= WINDOW_XY_OVERFLOW_THRESHOLD:
                    data[key] = WINDOW_XY_DEFAULT_OFFSET
                    LOGGER.debug(f"'{key}' found in '{file.name}' but with overflowed value, reset to '{key} = {WINDOW_XY_DEFAULT_OFFSET}'")
            file.write_text(sjson.dumps(data))
            edited_list.append(file)
        if edited_list:
            edited_list = '\n'.join(f"  - {file}" for file in edited_list)
            msg = f"""Applied custom resolution to:
{edited_list}"""
            LOGGER.info(msg)


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
