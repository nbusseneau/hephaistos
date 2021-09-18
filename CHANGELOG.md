# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

-   Improve Hades directory auto-detection on Windows using OS variables (drive- and architecture-agnostic).

### Fixed

-   Fix Hades window being positioned offscreen when switching to windowed mode while using a custom resolution larger than officially supported by the main monitor (multi-monitor use case).
-   Fix load screen transition clipping when passing through door Styx -> [Redacted] for 32-bit engine.
-   Fix Hades directory auto-detection not expanding user variables on MacOS / Linux.
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

-   Add MacOS and Linux binaries.

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

[Unreleased]: https://github.com/nbusseneau/hephaistos/compare/v1.4.1...HEAD

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
