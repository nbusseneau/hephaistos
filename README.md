# Hephaistos

https://user-images.githubusercontent.com/4659919/131267791-5e71f0e0-4496-4bf1-bc55-ab5e98eccc9a.mp4

CLI tool for patching any resolution in [Supergiant Games' Hades](https://store.steampowered.com/app/1145360/Hades/), primarily targeting ultrawide monitors (21:9, 32:9), multi-monitor (48:9), and Steam Deck (16:10).

By default, on Hades:

- Resolutions wider than 16:9 (e.g. 21:9) are pillarboxed with artwork / black bars on left / right.
- Resolutions taller than 16:9 (e.g. 16:10) are letterboxed with black bars on top / bottom.

Hephaistos can bypass both, and also allows using custom resolutions (useful for custom window sizes and multi-monitor without Eyefinity / Surround).

- For trying out Hephaistos right away, see [Install](#install).
- For a preview of how Hades looks in 21:9, 32:9, 48:9, and 16:10, see [Showcase](#showcase).
- For more details about how Hephaistos works, see [Under the hood](#under-the-hood).

# Issues

Hephaistos is in a stable state: many users have been using it for a long time (some of them even from their very first time on Hades), and nothing major has had to be fixed for a while.

Still, there might be some quirks or rare interactions on specific setups that haven't been detected yet: you are most welcome to report anything you witness by [opening a new issue](https://github.com/nbusseneau/hephaistos/issues/new) (ideally with screenshots / videos / a save file) and I will definitely have a look and fix it&nbsp;👌

# Showcase

<details>
<summary>21:9 (with HUD expanded)</summary>
  
![Tartarus_21-9](https://user-images.githubusercontent.com/4659919/131758654-652b8a8f-6bf9-472e-b645-98b257eaf05d.png)
![Athena_21-9](https://user-images.githubusercontent.com/4659919/131758678-340cbe57-bc92-473d-9df4-76f0e2b7470d.png)
![Boons_21-9](https://user-images.githubusercontent.com/4659919/178073900-dbcb9560-5635-444d-8327-676d2b316335.jpg)
![Combat_21-9](https://user-images.githubusercontent.com/4659919/178073861-1f73bcc2-69ca-4c01-91ee-a808c82e5a8a.jpg)
</details>

<details>
<summary>32:9 (with HUD expanded)</summary>
  
![Tartarus_32-9](https://user-images.githubusercontent.com/4659919/131758668-e2ace1db-fefa-4aa8-a1de-d9271eeb5e3e.png)
![Athena_32-9](https://user-images.githubusercontent.com/4659919/131758683-2baf86f6-0214-4748-9e86-8cf3ee7c9e83.png)
![Boons_32-9](https://user-images.githubusercontent.com/4659919/178073909-3d955440-1bd7-4cc6-9fae-a06a2a1c39a9.jpg)
![Combat_32-9](https://user-images.githubusercontent.com/4659919/178073940-9e1963af-dac7-4317-ab81-57aa0b42f2a1.jpg)
</details>

<details>
<summary>48:9 / triple screen (with HUD centered)</summary>
  
![Tartarus_48-9_hud-center](https://user-images.githubusercontent.com/4659919/132792501-fcbcbf9a-5b02-4f2c-a6e3-da90fb7d0393.jpg)
![Athena_48-9_hud-center](https://user-images.githubusercontent.com/4659919/132792617-79dfd680-0102-4564-9944-d33fb2b057b8.jpg)
![Boons_48-9_hud-center](https://user-images.githubusercontent.com/4659919/178073914-473560fe-872b-47a9-b1d0-95152e92f11c.jpg)
![Combat_48-9_hud-center](https://user-images.githubusercontent.com/4659919/178073931-b43d2240-0a25-4554-aece-f9f306776d0a.jpg)
</details>

<details>
<summary>16:10 (with HUD expanded)</summary>
  
![Tartarus_16-10](https://user-images.githubusercontent.com/4659919/178074465-a920265d-401c-4adb-b7e5-37b50d334f3b.jpg)
![Athena_16-10](https://user-images.githubusercontent.com/4659919/178074470-0a0281ec-1fae-47e5-bd13-e57823629c71.jpg)
![Boons_16-10](https://user-images.githubusercontent.com/4659919/178074482-0d25d9da-4bb2-473a-9a4f-7c45bb666fa3.jpg)
![Combat_16-10](https://user-images.githubusercontent.com/4659919/178074474-fb093287-21f7-4356-b899-da9bbd2ea98e.jpg)
</details>

> ℹ️ More images can be found over at [Nexus Mods](https://www.nexusmods.com/hades/mods/107?tab=images) and [WSGF](https://www.wsgf.org/dr/hades/en).

# Install

## Download

Hephaistos can be downloaded as an executable for Windows, macOS, and Linux, or
as a Python archive:

<details>
<summary>Windows</summary>
  
- Download [hephaistos-windows.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-windows.zip).
- Extract the archive. You should get an `hephaistos.exe` executable.
- Move `hephaistos.exe` to Hades main directory. Hephaistos must be sitting right next to the default directories:
  - Steam / Epic Games
    ```
    Hades/
    ├── Content/
    ├── x64/
    ├── x64Vk/
    ├── x86/
    └── hephaistos.exe
    ```
    > ⚠️&nbsp;If you don't know where Hades is, Hephaistos can try to give you a tip by auto-detecting from Steam and Epic Games configuration files: just run `hephaistos.exe`.
    > Note that you still have to move the files to the Hades directory manually before continuing.
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
    > ⚠️&nbsp;If you don't know where Hades is, just reinstall Hades from the Microsoft Store: you can then choose where Hades will be located.
    > Note that you still have to move the files to the Hades directory manually before continuing.
</details>

<details>
<summary>macOS</summary>
  
- Download [hephaistos-macos.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-macos.zip).
- Extract the archive. You should get an `hephaistos` executable.
- Move `hephaistos` to Hades main directory. Hephaistos must be sitting right next to the default directories (Steam / Epic Games):
  ```
  Hades/
  ├── Game.macOS.app/
  └── hephaistos
  ```
  > ⚠️&nbsp;If you don't know where Hades is, Hephaistos can try to give you a tip by auto-detecting from Steam and Epic Games configuration files: just run `hephaistos`.
  > Note that you still have to move the files to the Hades directory manually before continuing.
</details>

<details>
<summary>Linux</summary>
  
- Download [hephaistos-linux.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-linux.zip).
- Extract the archive. You should get an `hephaistos` executable.
- Move `hephaistos` to Hades main directory. Hephaistos must be sitting right next to the default directories (Steam):
  ```
  Hades/
  ├── Content/
  ├── x64/
  ├── x64Vk/
  ├── x86/
  └── hephaistos
  ```
  > ⚠️&nbsp;If you don't know where Hades is, Hephaistos can try to give you a tip by auto-detecting from Steam configuration files: just run `hephaistos`.
  > Note that you still have to move the files to the Hades directory manually before continuing.
</details>

<details>
<summary><b>[Advanced]</b> Python</summary>
  
- Download [hephaistos-python.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-python.zip).
- Extract the archive. You should get `hephaistos`, `hephaistos-data` and `sjson` directories.
- Move all directories to Hades main directory. Hephaistos must be sitting right next to the default directories (see Windows / macOS / Linux entries above for more details).
</details>

## Usage

Once Hephaistos is placed in the proper directory, you can use it in two ways:

- **[Easy]** Directly run Hephaistos and follow the interactive instructions: see [Interactive mode](#interactive-mode) for detailed help.
- **[Advanced]** Use Hephaistos subcommands from the command line: see [CLI usage](#cli-usage) below.

# Interactive mode

- Windows: run `hephaistos.exe`
- macOS / Linux: run `hephaistos`
- Python: run `python -m hephaistos`

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
INFO:hephaistos:Using '--hud=expand': HUD will be expanded horizontally
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

# CLI usage

- Windows: run `hephaistos.exe -h`
- macOS / Linux: run `hephaistos -h`
- Python: run `python -m hephaistos -h`

Hephaistos is mostly self-documented via the CLI help.
Run `hephaistos -h` to find the available subcommands (`patch`, `restore`, etc.) which themselves are documented (e.g. `hephaistos patch -h`).

An optional `-v` flag may be passed to print some information about what Hephaistos is doing under the hood.
The flag may be repeated twice (`-vv`) for displaying debug output.

### Mod Importer

Hephaistos is compatible with Mod Importer[^modimporter] (>= 1.3.0).
If Hephaistos detects it is available, it will run `modimporter` to register / unregister itself during `patch` and `restore` operations, instead of manually editing `Content\Scripts\RoomManager.lua`.

This can be bypassed with `--no-modimporter`, in which case Hephaistos will not run `modimporter` even if detected.

## Patching Hades using Hephaistos

Adjusting `3440` and `1440` with your own resolution:

```bat
hephaistos patch 3440 1440
```

> ℹ️ You can safely repatch multiple times in a row as Hephaistos always patches based on the original files.
> There is no need to restore files in-between.

### HUD

By default, Hephaistos expands the HUD horizontally as wide as possible: left and right side HUD elements will respectively stay fixed on the left and right after resizing.
For 32:9 or wider resolutions, you might want to use `--hud=center` to keep the HUD in the center of the screen with the same width as the original 16:9 HUD.

### Scaling

Hephaistos supports the following scaling algorithms:

- `hor+` (Hor+ scaling): expand aspect ratio and field of view horizontally, keep vertical height / field of view. This is the default scaling used by Hephaistos for aspect ratios wider than 16:9 (e.g. 21:9), and recommended for general usage as it strives to keep the experience as close to the original as possible.
- `vert+` (Vert+ scaling): expand aspect ratio and field of view vertically, keep horizontal height / field of view. This is the default scaling used by Hephaistos for aspect ratios taller than 16:9 (e.g. 16:10), and recommended for general usage as it strives to keep the experience as close to the original as possible.
- `pixel` (pixel-based scaling): expand field of view in all directions without applying any scaling, disregarding aspect ratios. This scaling is not recommended for general usage as it effectively "zooms out" the camera and thus does not keep the experience close to the original, but it's fun if you have a big screen and want to see more of the screen at once.

Use `--scaling=pixel` if you wish to use pixel-based scaling.

### Custom resolution

By default, Hephaistos patches a custom resolution in the [`ProfileX.sjson` configuration file](https://www.pcgamingwiki.com/wiki/Hades#Configuration_file.28s.29_location), by updating its `WindowWidth`/`WindowHeight` and `X`/`Y` values.

This has two advantages:

- Ensure the game runs at the preferred resolution.
  - Useful for users which had inadvertently switched up their resolutions from the game settings.
- Allow running the game in windowed mode at a specific size.
  - Useful for choosing your own window size in windowed mode.
  - Useful for spanning the game window over multi-monitor without Eyefinity / Surround.
  - This was not possible by default as window size is static: only the resolutions from the main display are offered from the game settings and the game window cannot be freely resized.

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

# Under the hood

By default, Hades uses a 1920x1080 internal resolution (viewport) with static scaling (i.e. it can only played at 16:9, no matter the display resolution).

To bypass this limitation, Hephaistos patches the game's files with an ad-hoc viewport computed depending on chosen resolution and scaling algorithm:

```console
> hephaistos patch 3440 1440 -v
INFO:hephaistos:Using resolution: (3440, 1440)
INFO:hephaistos:Using '--scaling=hor+': computed patch viewport (2580, 1080)
INFO:hephaistos:Using '--hud=expand': HUD will be expanded horizontally
INFO:hephaistos:Patched 'x64\EngineWin64s.dll'
...
INFO:hephaistos:Installed Lua mod 'hephaistos/lua' to 'Content/Mods/Hephaistos'
INFO:hephaistos:Patched 'Content/Scripts/RoomManager.lua' with hook 'Import "../Mods/Hephaistos/Hephaistos.lua"'

> hephaistos patch 3440 1440 -v --scaling=pixel
INFO:hephaistos:Using resolution: (3440, 1440)
INFO:hephaistos:Using '--scaling=pixel': computed patch viewport (3440, 1440)
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
