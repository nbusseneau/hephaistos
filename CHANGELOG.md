# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

-   Fix Hephaistos closing instead of displaying suggestion to move to Hades directory when launched outside of Hades directory.

## [1.7.2] - 2022-07-23

### Added

-   Recommend users to update Mod Importer when it fails to run due to being outdated.

## [1.7.1] - 2022-07-14

### Fixed

-   Fix Mirror of Night "locked" bottom panel when in `vert+`.
-   Fix locked choice overlay (Approval Process pact) when in `vert+`.

## [1.7.0] - 2022-07-08

### Added

-   Add Vert+ scaling (`--scaling=vert+`) to support resolutions taller than 16:9 (e.g. Steam Deck's 16:10).
-   Add pixel-based scaling (`--scaling=pixel`) as an alternative to Hor+/Vert+ for those interested in seeing more at once by "zooming out" the camera.
-   Add 16:10 in interactive mode resolution selector.

### Changed

-   Auto-determine default scaling: `hor+` for wider aspect ratios / `vert+` for taller aspect ratios.
-   Complete refactoring of Lua functions hooking mechanism.

### Fixed

-   Fix Tight Deadline timer when using `--hud=center`.
-   Fix credits roll starting too high when using `--hud=center`.
-   Fix self-loaded bloodstones counter when using `--hud=center`.

## [1.6.4] - 2022-04-09

### Fixed

-   Fix Hephaistos for Hades update V1.38290 on macOS via Steam / Epic Games.
-   Fix macOS / Linux binaries not working with Python version of Mod Importer.

## [1.6.3] - 2022-02-28

### Fixed

-   Fix save directory path detection for Steam Play on Linux.
-   Fix `--hades-dir` not working (notably in conjunction with interactive mode and absolute paths).

## [1.6.2] - 2022-02-26

### Fixed

-   Fix Codex chapter arrow not being centred on chapter name.

## [1.6.1] - 2022-02-16

### Changed

-   When game updates happen, Hephaistos will now try to patch anyway (with warnings) instead of not patching (with errors).

### Fixed

-   Fix Hephaistos for Hades update V1.38290 on Windows / Linux via Steam / Epic Games.

## [1.6.0] - 2022-02-13

### Added

-   Add support for Microsoft Store version of Hades.

## [1.5.1] - 2022-02-06

### Fixed

-   Fix controller selection not working properly in menus on very wide aspect ratios (32:9 and above).

## [v1.5.0] - 2021-11-25

### Added

-   Add `modfile.txt` and allow using Mod Importer (>= 1.3.0) [\[1\]](https://github.com/SGG-Modding/sgg-mod-modimporter)[\[2\]](https://www.nexusmods.com/hades/mods/26) for registering Hephaistos in Hades' files.
-   Add Mod Utility (>= 2.2.0) [\[1\]](https://github.com/SGG-Modding/sgg-mod-modutil)[\[2\]](https://www.nexusmods.com/hades/mods/27) compatibility layer.

### Fixed

-   Fix missing room transition overlay scaling for surface rooms.

## [v1.4.6] - 2021-10-28

### Changed

-   Custom resolution is now set through `ProfileX.sjson` as the game now properly allows bypassing detected monitor resolutions. Engine-side custom resolution implementation has been removed.

### Fixed

-   Remove bypass for V1.38239 (released on 2021-10-07) following fix in V1.38246 (released on 2021-10-27).

## [v1.4.5] - 2021-10-08

### Changed

-   Improve `--force` to only replace backups / hashes for files with hash mismatch.

### Fixed

-   Implement bypass for V1.38239 (released on 2021-10-07) breaking monitor resolution detection logic even when unmodded. Hephaistos fixes the bug by bypassing this and forcing in its own custom resolution.
-   Fix `ProfileX.sjson` detection on Windows when the `Documents` directory has been moved elsewhere.
-   Fix `--force` patching on top of already patched files in case of game update.

## [v1.4.4] - 2021-10-03

### Changed

-   Better logging and resilience when not finding `ProfileX.sjson` for multi-monitor windowed mode offscreen safeguard.

### Fixed

-   Fix multi-monitor windowed mode offscreen safeguard not detecting `ProfileX.sjson` files on Windows with OneDrive enabled.

## [v1.4.3] - 2021-10-01

### Fixed

-   Fix patching to be compatible with the macOS version of the game.

## [v1.4.2] - 2021-09-18

### Changed

-   Improve Hades directory auto-detection on Windows using OS variables (drive- and architecture-agnostic).

### Fixed

-   Fix Hades window being positioned offscreen when switching to windowed mode while using a custom resolution larger than officially supported by the main monitor (multi-monitor use case).
-   Fix load screen transition clipping when passing through door Styx -> [Redacted] for 32-bit engine.
-   Fix Hades directory auto-detection not expanding user variables on macOS / Linux.
-   Fix Hades directory auto-detection not properly picking up Steam libraries.

## [v1.4.1] - 2021-09-15

### Fixed

-   Fix custom resolution not working when larger than officially supported by the main monitor (multi-monitor use case).

## [v1.4.0] - 2021-09-14

### Added

-   Use a custom resolution by default, bypassing monitor resolution detection (useful for custom window sizes and multi-monitor without Eyefinity / Surround).
-   Add optional `--no-custom-resolution` CLI flag to allow keeping regular monitor resolution detection.

### Removed

-   Remove `-s` CLI shorthand for `--scaling`.

### Fixed

-   Fix `status` command unnecessarily copying Lua mod directory.
-   Fix `status` command not working with new camera clamping and mouse control hex patched fixes.

## [v1.3.2] - 2021-09-12

### Fixed

-   Fix camera mouse control reference point being locked to original viewport center `(960,540)`.
-   Fix camera clamping effect bugging out in instances where original clamp weight was `0.0`.

## [v1.3.1] - 2021-09-11

### Fixed

-   Fix camera clamping effect onto points of interest e.g. exit doors (especially at larger viewports such as 32:9 or 48:9, where the camera was not following Zagreus anymore).

## [v1.3.0] - 2021-09-10

### Added

-   Add optional `--hud` CLI flag to allow choosing between expanding HUD horizontally (default) or centering the HUD.

### Changed

-   Offer to choose between expanding and centering HUD when using interactive mode.
-   Offer to pick from 48:9 / triple screen resolutions when using interactive mode.

### Fixed

-   Fix SJON patching artefacts in `Height` and `Y` values when using pixel-based scaling.

## [v1.2.0] - 2021-09-06

### Added

-   Bundle `hephaistos-data` internally with standalone executables.
-   Add version info to Windows executable.

### Changed

-   Use PyInstaller 4.0 rather than 4.3 in order to remove false positive detections from AV software.

### Fixed

-   Fix version check debug log being incorrectly displayed in interactive mode.

## [v1.1.1] - 2021-09-05

### Fixed

-   Fix incorrect `Current version` being displayed by `version` for artifacts built from GitHub.

## [v1.1.0] - 2021-09-04

### Added

-   Add new `status` subcommand to check Hades / Hephaistos status (also available in interactive mode).
-   Add new `version` subcommand to check Hephaistos version and if Hephaistos is up to date.

### Changed

-   Interactive mode now displays current / latest version and links to latest version if an update is available.

## [v1.0.1] - 2021-09-03

### Fixed

-   Fix load screen transition clipping when passing through door Styx -> [Redacted] for DirectX 64-bit and Vulkan engines.
-   Fix biome map first time reward icon scaling.

## [v1.0.0] - 2021-09-01

### Changed

-   Hephaistos has graduated out of alpha and is now published on [Nexus Mods](https://www.nexusmods.com/hades/mods/107).

## [v0.13.0] - 2021-09-01

### Changed

-   Manually recenter run clear screen elements for a closer to original look.

### Fixed

-   Fix Hephaistos not working for new save slots.

## [v0.12.0] - 2021-08-22

### Fixed

-   Fix end credits.
-   Fix mid-run trait UI (B button) bottom graphics.

## [v0.11.0] - 2021-08-22

### Changed

-   Switch scaled backgrounds/overlays from uniform scaling to independent X/Y scaling.

### Fixed

-   Fix death background incorrectly scaling.
-   Fix practically all overlays/backgrounds.

## [v0.10.0] - 2021-08-22

### Fixed

-   Fix text overflowing out of GUI components.
-   Properly scale vignettes displayed when hit (blood frame, boiling blood, poison, lava).
-   Re-fix world map shown between regions (oops :D).
-   Fix full screen displacement FX for various occasions (calls, Chaos interact, Hades speaking, etc.).
-   Fix assist/summon (e.g. Sisyphus) overlay.
-   Fix epilogue sigils.

## [v0.9.0] - 2021-08-21

### Fixed

-   Fix locked keepsakes icons.
-   Fix top left icon on boon choice menu.
-   Fix reroll vignette overlay.
-   Fix gun ammo UI being offset to the right.

## [v0.8.0] - 2021-08-19

### Fixed

-   Fix screen flashes when getting hit.
-   Fix boon info screen.
-   Fix mid-run trait overlay (B button header).
-   Fix world map shown between regions.
-   Fix quest log (fates) scroll up/down buttons.

## [v0.7.0] - 2021-08-19

### Fixed

-   Fix `Screen*` Lua state variables being overwritten in save file and incorrectly kept after Hephaistos was removed.
-   Fix a bunch of screens: codex, contractor.

## [v0.6.0] - 2021-08-15

### Fixed

-   Fix a bunch of overlays (notably shops).
-   Fix a bunch of screens: quest log (fates), run history, mirror of night, pact of punishment, weapon upgrade, keepsakes.

## [v0.5.0] - 2021-08-15

### Added

-   Support `--force` in interactive mode to allow users to repatch after a game update.
-   Support specifying a custom resolution in interactive mode.

### Changed

-   Loop interactive mode instead of auto-closing, users may exit using the dedicated option.
-   Split 21:9 and 31:9 resolutions in interactive mode selector.

### Fixed

-   Fix arrow keys registering multiple keypresses in interactive mode.

## [v0.4.0] - 2021-08-15

### Added

-   Add macOS and Linux binaries.

### Changed

-   Move data (backups, hashes, Lua source) from `hephaistos` to `hephaistos-data`

## [v0.3.0] - 2021-08-14

### Added

-   Interactive mode when running Hephaistos without any additional arguments.
-   Check if Hephaistos is properly placed in the Hades directory.
-   Try to auto-detect Hades directory and advise user to move Hephaistos there.

### Changed

-   Improve logging.
-   Switch to helpers for Lua mod init state fix calculations.
-   Refactor safe patching with a context manager.

### Fixed

-   Fix Lua mod relative imports not being configured properly.

## [v0.2.0] - 2021-08-12

### Changed

-   Complete refactoring with initial support for GUI patching (SJSON + Lua).

## [v0.1.0] - 2021-05-24

### Added

-   Initial release.

[Unreleased]: https://github.com/nbusseneau/hephaistos/compare/v1.7.2...HEAD

[1.7.2]: https://github.com/nbusseneau/hephaistos/compare/v1.7.1...v1.7.2

[1.7.1]: https://github.com/nbusseneau/hephaistos/compare/v1.7.0...v1.7.1

[1.7.0]: https://github.com/nbusseneau/hephaistos/compare/v1.6.4...v1.7.0

[1.6.4]: https://github.com/nbusseneau/hephaistos/compare/v1.6.3...v1.6.4

[1.6.3]: https://github.com/nbusseneau/hephaistos/compare/v1.6.2...v1.6.3

[1.6.2]: https://github.com/nbusseneau/hephaistos/compare/v1.6.1...v1.6.2

[1.6.1]: https://github.com/nbusseneau/hephaistos/compare/v1.6.0...v1.6.1

[1.6.0]: https://github.com/nbusseneau/hephaistos/compare/v1.5.1...v1.6.0

[1.5.1]: https://github.com/nbusseneau/hephaistos/compare/v1.5.0...v1.5.1

[v1.5.0]: https://github.com/nbusseneau/hephaistos/compare/v1.4.6...v1.5.0

[v1.4.6]: https://github.com/nbusseneau/hephaistos/compare/v1.4.5...v1.4.6

[v1.4.5]: https://github.com/nbusseneau/hephaistos/compare/v1.4.4...v1.4.5

[v1.4.4]: https://github.com/nbusseneau/hephaistos/compare/v1.4.3...v1.4.4

[v1.4.3]: https://github.com/nbusseneau/hephaistos/compare/v1.4.2...v1.4.3

[v1.4.2]: https://github.com/nbusseneau/hephaistos/compare/v1.4.1...v1.4.2

[v1.4.1]: https://github.com/nbusseneau/hephaistos/compare/v1.4.0...v1.4.1

[v1.4.0]: https://github.com/nbusseneau/hephaistos/compare/v1.3.2...v1.4.0

[v1.3.2]: https://github.com/nbusseneau/hephaistos/compare/v1.3.1...v1.3.2

[v1.3.1]: https://github.com/nbusseneau/hephaistos/compare/v1.3.0...v1.3.1

[v1.3.0]: https://github.com/nbusseneau/hephaistos/compare/v1.2.0...v1.3.0

[v1.2.0]: https://github.com/nbusseneau/hephaistos/compare/v1.1.1...v1.2.0

[v1.1.1]: https://github.com/nbusseneau/hephaistos/compare/v1.1.0...v1.1.1

[v1.1.0]: https://github.com/nbusseneau/hephaistos/compare/v1.0.1...v1.1.0

[v1.0.1]: https://github.com/nbusseneau/hephaistos/compare/v1.0.0...v1.0.1

[v1.0.0]: https://github.com/nbusseneau/hephaistos/compare/v0.13.0...v1.0.0

[v0.13.0]: https://github.com/nbusseneau/hephaistos/compare/v0.12.0...v0.13.0

[v0.12.0]: https://github.com/nbusseneau/hephaistos/compare/v0.11.0...v0.12.0

[v0.11.0]: https://github.com/nbusseneau/hephaistos/compare/v0.10.0...v0.11.0

[v0.10.0]: https://github.com/nbusseneau/hephaistos/compare/v0.9.0...v0.10.0

[v0.9.0]: https://github.com/nbusseneau/hephaistos/compare/v0.8.0...v0.9.0

[v0.8.0]: https://github.com/nbusseneau/hephaistos/compare/v0.7.0...v0.8.0

[v0.7.0]: https://github.com/nbusseneau/hephaistos/compare/v0.6.0...v0.7.0

[v0.6.0]: https://github.com/nbusseneau/hephaistos/compare/v0.5.0...v0.6.0

[v0.5.0]: https://github.com/nbusseneau/hephaistos/compare/v0.4.0...v0.5.0

[v0.4.0]: https://github.com/nbusseneau/hephaistos/compare/v0.3.0...v0.4.0

[v0.3.0]: https://github.com/nbusseneau/hephaistos/compare/v0.2.0...v0.3.0

[v0.2.0]: https://github.com/nbusseneau/hephaistos/compare/v0.1.0...v0.2.0

[v0.1.0]: https://github.com/nbusseneau/hephaistos/compare/26a8fd00a6db8e1d513879569f70b6ea51a9e0c6...v0.1.0
