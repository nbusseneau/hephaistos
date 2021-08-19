# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/nbusseneau/hephaistos/compare/v0.7.0...HEAD

[v0.7.0]: https://github.com/nbusseneau/hephaistos/compare/v0.6.0...v0.7.0

[v0.6.0]: https://github.com/nbusseneau/hephaistos/compare/v0.5.0...v0.6.0

[v0.5.0]: https://github.com/nbusseneau/hephaistos/compare/v0.4.0...v0.5.0

[v0.4.0]: https://github.com/nbusseneau/hephaistos/compare/v0.3.0...v0.4.0

[v0.3.0]: https://github.com/nbusseneau/hephaistos/compare/v0.2.0...v0.3.0

[v0.2.0]: https://github.com/nbusseneau/hephaistos/compare/v0.1.0...v0.2.0

[v0.1.0]: https://github.com/nbusseneau/hephaistos/compare/26a8fd00a6db8e1d513879569f70b6ea51a9e0c6...v0.1.0
