# Hephaistos

[![GitHub Actions status](https://img.shields.io/github/workflow/status/nbusseneau/hephaistos/Release/main)](https://github.com/nbusseneau/hephaistos/actions/workflows/build-release.yaml?query=branch%3Amain)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/nbusseneau/hephaistos)](https://github.com/nbusseneau/hephaistos/releases/latest)
[![GitHub downloads](https://img.shields.io/github/downloads/nbusseneau/hephaistos/total)](https://github.com/nbusseneau/hephaistos/releases)
[![GitHub stars](https://img.shields.io/github/stars/nbusseneau/hephaistos)](https://github.com/nbusseneau/hephaistos/stargazers)
[![GitHub license](https://img.shields.io/github/license/nbusseneau/hephaistos)](https://github.com/nbusseneau/hephaistos/blob/main/LICENSE)

https://user-images.githubusercontent.com/4659919/131267791-5e71f0e0-4496-4bf1-bc55-ab5e98eccc9a.mp4

CLI tool for patching any resolution in [Supergiant Games' Hades](https://store.steampowered.com/app/1145360/Hades/), primarily targeting ultrawide monitors (21:9, 32:9), multi-monitor (48:9), and Steam Deck (16:10).

By default, on Hades:

- Resolutions wider than 16:9 (e.g. 21:9) are pillarboxed with artwork / black bars on left / right.
- Resolutions taller than 16:9 (e.g. 16:10) are letterboxed with black bars on top / bottom.

Hephaistos can bypass both, and also allows using custom resolutions (useful for custom window sizes and multi-monitor without Eyefinity / Surround).

**(Click on items to show details. For example, click on [Install](#install) for installation instructions.)**

<details>
<summary><h1>Issues</h1></summary>

Hephaistos is in a stable state: many users have been using it for a long time (some of them even from their very first time on Hades), and nothing major has had to be fixed for a while.

Still, there might be some quirks or rare interactions on specific setups that haven't been detected yet: you are most welcome to report anything you witness by [opening a new issue](https://github.com/nbusseneau/hephaistos/issues/new) (ideally with screenshots / videos / a save file) and I will definitely have a look and fix it&nbsp;👌

</details>

<details>
<summary><h1>Preview / Showcase</h1></summary>

## Before / after comparisons

**(Click on items to show details)**

<details>
<summary>21:9</summary>

![21-9_vanilla](https://user-images.githubusercontent.com/4659919/178168394-99b68f49-b391-4fa9-9f5b-89be99981a91.jpg)
![21-9_hephaistos](https://user-images.githubusercontent.com/4659919/178168395-2f730460-a8c8-4d11-8a35-8f3b0c003626.jpg)

</details>

<details>
<summary>32:9</summary>

![32-9_vanilla](https://user-images.githubusercontent.com/4659919/178283682-45ed919f-a156-4fab-a977-137cf711651e.jpg)
![32-9_hephaistos](https://user-images.githubusercontent.com/4659919/178281266-73f3e3f2-f47a-4d91-8705-16c3d8274ba2.jpg)

</details>

<details>
<summary>48:9 / triple screen (with HUD centered)</summary>

![48-9_vanilla](https://user-images.githubusercontent.com/4659919/178281805-5c43f3e4-cdde-44cb-ba26-e5648c054007.jpg)
![48-9_hephaistos](https://user-images.githubusercontent.com/4659919/178281402-53ad9ba3-32a4-4906-b6f5-0127e13991a1.jpg)

</details>

<details>
<summary>16:10 / Steam Deck</summary>

![SteamDeck](https://user-images.githubusercontent.com/4659919/178277503-b13e6e74-9527-41dd-8cf4-d52fee010b64.jpg)

</details>

## Additional screenshots

**(Click on items to show details)**

<details>
<summary>21:9</summary>

<img src="https://user-images.githubusercontent.com/4659919/131758654-652b8a8f-6bf9-472e-b645-98b257eaf05d.png" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/131758678-340cbe57-bc92-473d-9df4-76f0e2b7470d.png" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/178073900-dbcb9560-5635-444d-8327-676d2b316335.jpg" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/178073861-1f73bcc2-69ca-4c01-91ee-a808c82e5a8a.jpg" width="45%"></img>

</details>

<details>
<summary>32:9</summary>

<img src="https://user-images.githubusercontent.com/4659919/131758668-e2ace1db-fefa-4aa8-a1de-d9271eeb5e3e.png" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/131758683-2baf86f6-0214-4748-9e86-8cf3ee7c9e83.png" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/178073909-3d955440-1bd7-4cc6-9fae-a06a2a1c39a9.jpg" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/178073940-9e1963af-dac7-4317-ab81-57aa0b42f2a1.jpg" width="45%"></img>

</details>

<details>
<summary>48:9 / triple screen (with HUD centered)</summary>

<img src="https://user-images.githubusercontent.com/4659919/132792501-fcbcbf9a-5b02-4f2c-a6e3-da90fb7d0393.jpg" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/132792617-79dfd680-0102-4564-9944-d33fb2b057b8.jpg" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/178073914-473560fe-872b-47a9-b1d0-95152e92f11c.jpg" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/178073931-b43d2240-0a25-4554-aece-f9f306776d0a.jpg" width="45%"></img>

</details>

<details>
<summary>16:10 / Steam Deck</summary>

<img src="https://user-images.githubusercontent.com/4659919/178074465-a920265d-401c-4adb-b7e5-37b50d334f3b.jpg" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/178074470-0a0281ec-1fae-47e5-bd13-e57823629c71.jpg" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/178074482-0d25d9da-4bb2-473a-9a4f-7c45bb666fa3.jpg" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/178074474-fb093287-21f7-4356-b899-da9bbd2ea98e.jpg" width="45%"></img>

</details>

> ℹ️ More images can be found over at [Nexus Mods](https://www.nexusmods.com/hades/mods/107?tab=images) and [WSGF](https://www.wsgf.org/dr/hades/en).

</details>

<details>
<summary><h1>Install</h1></summary>

Hephaistos can be downloaded as an executable for Windows, macOS, and Linux, or as a Python archive, and must be placed in the `Hades` directory. **(Click on items to show details)**

<details>
<summary>Windows</summary>

- Download [hephaistos-windows.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-windows.zip).
- Extract the archive. You should get an `hephaistos.exe` executable.
- Move `hephaistos.exe` to the `Hades` directory. It must be placed right next to the default Hades files:
  - Steam / Epic Games / Heroic
    ```
    Hades/
    ├── Content/
    ├── x64/
    ├── x64Vk/
    ├── x86/
    └── hephaistos.exe
    ```
    > ⚠️&nbsp;If you don't know where `Hades` is, Hephaistos can try to give you a tip by auto-detecting from Steam / Epic Games / Heroic configuration files: double-click `hephaistos.exe`.
    > Note that you still have to move `hephaistos.exe` to the `Hades` directory manually before continuing.
  - Microsoft Store
    ```
    Hades/
    ├── Content/
    │   ├── Content/
    │   ├── ja/
    │   ├── Hades.exe
    │   └── ...
    ├── [hidden file] E0A69B86-F3DD-416D-BCA8-3782255B0B74
    ├── [hidden file] ...
    └── hephaistos.exe
    ```
    > ⚠️&nbsp;If you don't know where `Hades` is, reinstall Hades from the Microsoft Store: you can then choose where Hades will be located.
    > Note that you still have to move `hephaistos.exe` to the `Hades` directory manually before continuing.
    </details>

<details>
<summary>macOS</summary>

- Download [hephaistos-macos.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-macos.zip).
- Extract the archive. You should get an `hephaistos` executable.
- Move `hephaistos` to the `Hades` directory. It must be placed right next to the default Hades files:
  ```
  Hades/
  ├── Game.macOS.app/
  └── hephaistos
  ```
  > ⚠️&nbsp;If you don't know where `Hades` is, Hephaistos can try to give you a tip by auto-detecting from Steam / Epic Games configuration files: drag the `hephaistos` file onto the Terminal application icon and run it.
  > Note that you still have to move `hephaistos` to the `Hades` directory manually before continuing.
  </details>

<details>
<summary>Linux / Steam Deck</summary>

- Download [hephaistos-linux.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-linux.zip).
- Extract the archive. You should get an `hephaistos` executable.
- Move `hephaistos` to the `Hades` directory. It must be placed right next to the default Hades files:
  ```
  Hades/
  ├── Content/
  ├── x64/
  ├── x64Vk/
  ├── x86/
  └── hephaistos
  ```
  > ⚠️&nbsp;If you don't know where `Hades` is, Hephaistos can try to give you a tip by auto-detecting from Steam / Heroic configuration files: run `./hephaistos` in terminal (on Steam Deck: right-click > `Run in Konsole`).
  > Note that you still have to move `hephaistos` to the `Hades` directory manually before continuing.
  </details>

<details>
<summary><b>[Advanced]</b> Python</summary>

- Download [hephaistos-python.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-python.zip).
- Extract the archive. You should get `hephaistos`, `hephaistos-data` and `sjson` directories.
- Move all directories to the `Hades` directory. They must be placed right next to the default Hades files (see Windows / macOS / Linux entries above for more details).
</details>

Once Hephaistos is placed in the `Hades` directory, you are ready to use it:

- **[Easy]** Use Hephaistos' interactive instructions: see [Interactive mode](#interactive-mode).
- **[Advanced]** Use Hephaistos subcommands from the command line: see [CLI usage](#cli-usage).

</details>

<details>
<summary><h1>Interactive mode</h1></summary>

- **Windows:** double-click on `hephaistos.exe`
- **macOS:** drag the `Hades` directory onto the Terminal application icon > run `./hephaistos`
- **Linux / Steam Deck:** run `./hephaistos` in terminal (on Steam Deck: right-click > `Run in Konsole`)
- **Python:** run `python -m hephaistos`

When running Hephaistos in interactive mode, Hephaistos will guide you through the steps:

```
Hi! This interactive wizard will help you to set up Hephaistos.
Note: while Hephaistos can be used in interactive mode for basic usage, you will need to switch to non-interactive mode for any advanced usage. See the README for more details.

Current version: v1.x.y
Latest version: v1.x.y

Pick an option:
1. Patch Hades using Hephaistos
2. Restore Hades to its pre-Hephaistos state
3. Check current Hades / Hephaistos status
4. Exit
Choice:
```

Type `1` to pick the patch option. Hephaistos will again prompt you for your resolution and HUD preferences, and then patch Hades:

```
INFO:hephaistos:Using resolution: (3840, 1600)
INFO:hephaistos:Using '--scaling=hor+': computed patch viewport (2592, 1080)
INFO:hephaistos:Using '--hud=expand': HUD will be expanded horizontally / vertically
INFO:hephaistos:Patched 'x64\EngineWin64s.dll'
INFO:hephaistos:Reading SJSON data (this operation can take time, please be patient)
...
INFO:hephaistos:Installed Lua mod to 'Content\Mods\Hephaistos'
INFO:hephaistos:Patched 'Content\Scripts\RoomManager.lua' with hook 'Import "../Mods/Hephaistos/Hephaistos.lua"'

Press any key to continue...
```

> ⚠️&nbsp;Reading SJSON data can take time depending on your CPU and hard drive, please be patient&nbsp;⏳

Hades binaries are now patched to work with the chosen resolution.
Start the game and try it out for a bit.

Once done, use Hephaistos again, but this time type `2` to pick the restore option:

```
INFO:hephaistos:Restored backups from 'hephaistos-data\backups' to '.'
INFO:hephaistos:Discarded hashes at 'hephaistos-data\hashes'
INFO:hephaistos:Discarded SJSON data at 'hephaistos-data\sjson-data'
INFO:hephaistos:Uninstalled Lua mod from 'Content\Mods\Hephaistos'
```

Hades binaries are now restored to their pre-Hephaistos state.

Do note that every time it receives an update, Hades will automatically revert to its default resolution, and Hephaistos must be reapplied.
If in doubt, type `3` to pick the status option and check the current Hades / Hephaistos status.

This concludes the tutorial.
I hope you'll enjoy Hephaistos&nbsp;🥳

</details>

<details>
<summary><h1>CLI usage</h1></summary>

- **Executable:** `hephaistos -h`
- **Python:** `python -m hephaistos -h`

Hephaistos is mostly self-documented via the CLI help.
Use `hephaistos -h` to find the available subcommands (`patch`, `restore`, etc.) which themselves are documented (e.g. `hephaistos patch -h`).

Add the `-v` flag to print information about what Hephaistos is doing under the hood.
The flag may be repeated twice (`-vv`) to display debug output.

## Patching Hades using Hephaistos

Adjusting `3440` and `1440` with your own resolution:

```bat
hephaistos patch 3440 1440
```

> ℹ️ You can safely repatch multiple times in a row as Hephaistos always patches based on the original files.
> There is no need to restore files in-between.

### HUD

Hephaistos supports the following HUD resizing modes: **(Click on items to show details)**

<details>
<summary><code>expand</code> (default)</summary>

Expand the HUD horizontally and vertically, i.e. HUD will scale with screen size.
Static HUD elements will be repositioned to their intended location for the new screen size, e.g. health indicator will be in the bottom left, resource indicator will be in the bottom right.

![hud_21-9-vanilla](https://user-images.githubusercontent.com/4659919/178168394-99b68f49-b391-4fa9-9f5b-89be99981a91.jpg)
![hud_21-9_expand](https://user-images.githubusercontent.com/4659919/178168395-2f730460-a8c8-4d11-8a35-8f3b0c003626.jpg)

</details>

<details>
<summary><code>center</code></summary>

Keep HUD in the center of the screen with the same size as the original HUD, i.e. screen size will change but HUD will not move.

![hud_21-9-vanilla](https://user-images.githubusercontent.com/4659919/178168394-99b68f49-b391-4fa9-9f5b-89be99981a91.jpg)
![hud_21-9_center](https://user-images.githubusercontent.com/4659919/178168396-37eb931d-0158-409c-8e8d-702e37fa5435.jpg)

</details>

You might want to use `--hud=center` for 32:9 or wider resolutions.

### Scaling

Hephaistos supports the following scaling algorithms: **(Click on items to show details)**

<details>
<summary><code>hor+</code> (Hor+ scaling, default)</summary>

Expand aspect ratio and field of view horizontally, keep vertical height / field of view.
This is the default scaling used by Hephaistos for aspect ratios wider than 16:9 (e.g. 21:9), and recommended for general usage as it strives to keep the experience as close to the original as possible.

![scaling_21-9_vanilla](https://user-images.githubusercontent.com/4659919/178168549-5123c4fd-2d35-4f6a-904c-3112806bafb7.jpg)
![scaling_21-9_hor+](https://user-images.githubusercontent.com/4659919/178168543-66e6d0e3-ecd9-4903-bfd1-20062822a31b.jpg)

</details>

<details>
<summary><code>vert+</code> (Vert+ scaling, default)</summary>

Expand aspect ratio and field of view vertically, keep horizontal height / field of view.
This is the default scaling used by Hephaistos for aspect ratios taller than 16:9 (e.g. 16:10), and recommended for general usage as it strives to keep the experience as close to the original as possible.

<img src="https://user-images.githubusercontent.com/4659919/178176245-1b790773-7355-4f42-ac6b-15e4e649aa30.jpg" width="45%"></img> <img src="https://user-images.githubusercontent.com/4659919/178168540-bfebde73-d906-4f3b-9cc2-fa83a50f2f28.jpg" width="45%"></img>

</details>

<details>
<summary><code>pixel</code> (pixel-based scaling)</summary>

Expand field of view in all directions without applying any scaling, disregarding aspect ratios.
This scaling is not recommended for general usage as it effectively "zooms out" the camera and thus does not keep the experience close to the original, but it's fun if you have a big screen and want to see more of the screen at once.

![scaling_21-9_vanilla](https://user-images.githubusercontent.com/4659919/178168549-5123c4fd-2d35-4f6a-904c-3112806bafb7.jpg)
![scaling_21-9_pixel](https://user-images.githubusercontent.com/4659919/178168547-0f20a2fa-76ef-4a33-8ea9-a4abb0cedb6b.jpg)

</details>

Use `--scaling=pixel` if you wish to use pixel-based scaling.

### Custom resolution

By default, Hephaistos patches a custom resolution in the [`ProfileX.sjson` configuration file](https://www.pcgamingwiki.com/wiki/Hades#Configuration_file.28s.29_location) by updating its `WindowWidth`/`WindowHeight` and `X`/`Y` values.

This has two advantages:

- Ensure the game runs at the preferred resolution.
  - Useful when inadvertently switching to a wrong resolution from the game settings.
  - Useful when playing Hades on a secondary monitor.
- Allow running the game in windowed mode at a specific size.
  - Useful for choosing your own window size in windowed mode.
  - Useful for spanning the game window over multi-monitor without Eyefinity / Surround.

Neither of these are possible in the vanilla game: only the resolutions from the main display are offered from the game settings and the game window cannot be freely resized.

Use `--no-custom-resolution` if you wish not to force custom resolution through `ProfileX.sjson`.

## Restoring Hades to its pre-Hephaistos state

```bat
hephaistos restore
```

## Checking Hades / Hephaistos status

```bat
hephaistos status
```

## Patching Hades again after a game update

Every time it receives an update, Hades will automatically revert to its default resolution, and Hephaistos must be reapplied.
Trying to repatch after a game update will be blocked:

```console
> hephaistos patch 3440 1440
ERROR:hephaistos:Hash file mismatch: 'XXX' was modified.
ERROR:hephaistos:Was the game updated? Re-run with '--force' to discard previous backups and re-patch Hades from its current state.
```

And status will confirm this:

```console
> hephaistos status
Hades was patched with Hephaistos, but Hades files were modified. Was the game updated?
```

Since the game was updated, the previous backups can be safely discarded.
Use `--force` to repatch and create new backups:

```bat
hephaistos patch 3440 1440 --force
```

## Miscellaneous options

### `Hades` directory

By default, Hephaistos assumes that it has been placed in the `Hades` directory.
If it fails to detect Hades files, it will try to auto-detect `Hades` location from Steam / Epic Games / Heroic configuration files and ask to be relocated.

You may use `--hades-dir` to manually specify where `Hades` is located, e.g. if you want to store Hephaistos and its files in a different location than the `Hades` directory.

### Mod Importer

Hephaistos is compatible with Mod Importer[^modimporter] (>= 1.3.0).
If Hephaistos detects it is available, it will run `modimporter` to register / unregister itself during `patch` and `restore` operations, instead of manually editing `Content\Scripts\RoomManager.lua`.

This can be bypassed with `--no-modimporter`, in which case Hephaistos will not run `modimporter` even if detected.

</details>

<details>
<summary><h1>Under the hood</h1></summary>

Hades uses an internal 1920x1080 viewport with static scaling (i.e. it can only played at 16:9, no matter the display resolution).

To bypass this limitation, Hephaistos patches the game's files with an ad-hoc viewport computed depending on chosen resolution and scaling algorithm:

```console
> hephaistos patch 3440 1440 -v
INFO:hephaistos:Using resolution: (3440, 1440)
INFO:hephaistos:Using '--scaling=hor+': computed patch viewport (2580, 1080)
INFO:hephaistos:Using '--hud=expand': HUD will be expanded horizontally / vertically
INFO:hephaistos:Patched 'x64\EngineWin64s.dll'
...
INFO:hephaistos:Installed Lua mod 'hephaistos/lua' to 'Content/Mods/Hephaistos'
INFO:hephaistos:Patched 'Content/Scripts/RoomManager.lua' with hook 'Import "../Mods/Hephaistos/Hephaistos.lua"'

> hephaistos patch 1280 800 -v
INFO:hephaistos:Using resolution: (1280, 800)
INFO:hephaistos:Using '--scaling=vert+': computed patch viewport (1920, 1200)
...
```

- Backends' engine DLLs are hex patched to expand the resolution and camera viewports.
- Resource SJSON files are patched to resize / move around GUI elements.
- Gameplay Lua scripts are extended with a Lua mod recalculating sizes / positions of GUI elements.

> ℹ️ Hephaistos is compatible with Mod Utility[^modutil] (>= 2.2.0). If available, it will leverage `ModUtil` hook functions rather than its own custom hooks.
> This makes Hephaistos more compatible with other `ModUtil`-based mods if they also are hooking onto the same functions as Hephaistos (though it still won't magically fix conflicts or new GUI elements from other mods that Hephaistos wasn't tailored to).

While patching, Hephaistos stores:

- A backup of the original files.
  - Allows restoring Hades to its pre-patch state if need be.
- File hashes of the patched files.
  - Allows detecting any outside modifications made to the files -- mostly for detecting game updates.
  - Allows detecting if we are repatching a previously patched installation, in which case the original files are used as basis for in-place repatching without an intermediate restore operation.
- (If patching an SJSON) A JSON-serialized `dict` of the deserialized original SJSON data.
  - Speeds up in-place repatching as we avoid the need to deserialize the original SJSON data again (which is very slow, while deserializing the JSON is instantaneous).

Everything is stored under the `hephaistos-data` directory.

## Why did you make this, and how did you know what to patch?

I love Hades and am an ultrawide player myself.
I decided to try my hand at modding ultrawide support by decompiling Hades and reverse-engineering the viewport logic just to see if I could, and here we are&nbsp;😄

See [this blog post](https://nicolas.busseneau.fr/en/blog/2021/04/hades-ultrawide-mod) for more details about Hephaistos' genesis.

[^modimporter]: Mod Importer ([GitHub](https://github.com/SGG-Modding/sgg-mod-modimporter) / [Nexus Mods](https://www.nexusmods.com/hades/mods/26)) is a tool helping to manage mods and register / unregister them with Hades.
[^modutil]: Mod Utility ([GitHub](https://github.com/SGG-Modding/sgg-mod-modutil) / [Nexus Mods](https://www.nexusmods.com/hades/mods/27)) is a mod-library helping mods integrate not only with Hades but also with other mods.

</details>
