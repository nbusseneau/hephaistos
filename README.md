# Hephaistos

![screenshot_3840x1600](https://user-images.githubusercontent.com/4659919/119279618-1cf06980-bc2d-11eb-8185-5915cbeda1e4.png)

CLI tool for patching any resolution in [Supergiant Games' Hades](https://store.steampowered.com/app/1145360/Hades/), initially intended as an ultrawide support mod.
It can bypass both pillarboxing and letterboxing, which are the default on non-16:9 resolutions for Hades.

- For trying out Hephaistos, see [Install](#install) below.
- For more details about how Hephaistos works, see [Under the hood](#under-the-hood).

## Video

https://user-images.githubusercontent.com/4659919/119279604-09dd9980-bc2d-11eb-964a-7893a57fe814.mp4

## Limitations

Hephaistos patches the engine and tries its best for patching the GUI, however GUI support is incomplete at the moment.
The game is 100% playable, but you may experience GUI artifacts, notably:

- Vignettes / overlays not taking up the whole screen.
- Text elements misplaced relative to their GUI boundaries.

Please report anything you encounter in [issue #1](https://github.com/nbusseneau/hephaistos/issues/1), ideally with screenshots / videos&nbsp;👌

## Install

- Download one of:
  - **[Recommended]** Standalone executable:
    - Windows: [hephaistos-windows.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-windows.zip)
    - MacOS: [hephaistos-macos.tar](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-macos.tar)
    - Linux: [hephaistos-linux.tar](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-linux.tar)
  - Python version: [hephaistos-python.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-python.zip)
- Extract the archive. You should see:
  - Standalone executable: `hephaistos.exe` or `hephaistos` executable and `hephaistos-data` directory.
  - Python version: `hephaistos`, `hephaistos-data` and `sjson` directories.
- Move all Hephaistos files to Hades main directory. Hephaistos must be sitting right next to the default Hades directories:

```
Hades
├── Content
├── hephaistos-data
├── x64
├── x64Vk
├── x86
└── hephaistos.exe
```

> ⚠️ If you don't know where Hades is, Hephaistos can try to auto-detect it for you:
>
> - Windows: run `hephaistos.exe`
> - MacOS / Linux: run `hephaistos`
> - Python: run `python -m hephaistos`
>
> Note that you still have to move the files to the Hades directory manually.

Once Hephaistos is placed in the proper directory, you can use it in two ways:

- **[Easy]** Directly run Hephaistos to enter interactive mode, and follow the instructions: see [Tutorial](#tutorial) for detailed help.
- **[Advanced]** Run Hephaistos from the command line: see [CLI usage](#cli-usage) below.

## Tutorial

- Windows: run `hephaistos.exe`
- MacOS / Linux: run `hephaistos`
- Python: run `python -m hephaistos`

When running Hephaistos in interactive mode, Hephaistos will guide you through the steps:

```
Hi! This interactive wizard will help you to set up Hephaistos.
Note: while Hephaistos can be used in interactive mode for basic usage, you will need to switch to non-interactive mode for any advanced usage. See the README for more details.

Pick an option:
1. Patch Hades using Hephaistos
2. Restore Hades to its pre-Hephaistos state
3. Cancel
Choice:
```

Type `1` to pick the patch option. Hephaistos will again prompt you for your resolution, and then patch Hades:

```
INFO:hephaistos:Computed patch viewport (2592, 1080) using scaling hor+ from resolution (3840, 1600)
INFO:hephaistos:Patched 'x64\EngineWin64s.dll' with viewport (2592, 1080)
...
INFO:hephaistos:Installed Lua mod to 'Content\Mods\Hephaistos'
INFO:hephaistos:Patched 'Content\Scripts\RoomManager.lua' with hook 'Import "../Mods/Hephaistos/Hephaistos.lua"'
Press enter to exit...
```

Press `↵ Enter` to close Hephaistos.
Hades binaries are now patched to work with the chosen resolution.
Start the game and try it out for a bit.

Once done, launch Hephaistos again, but this time type `2` to pick the restore option:

```
INFO:hephaistos:Restored backups from 'hephaistos-data\backups' to '.'
INFO:hephaistos:Discarded hashes at 'hephaistos-data\hashes'
INFO:hephaistos:Uninstalled Lua mod from 'Content\Mods\Hephaistos'
```

Hades binaries are now restored to their original state.

Do note that every time it receives an update, Hades will automatically revert to its default resolution, and Hephaistos must be reapplied.

This concludes the tutorial.
I hope you'll enjoy Hephaistos&nbsp;🥳

## CLI usage

- Windows: run `hephaistos.exe -h`
- MacOS / Linux: run `hephaistos -h`
- Python: run `python -m hephaistos -h`

Hephaistos is mostly self-documented via the CLI help.
Run `hephaistos -h` to find the available subcommands (`patch`, `restore`, etc.) which themselves are documented (e.g. `hephaistos patch -h`).

An optional `-v` flag may be passed to print some information about what Hephaistos is doing under the hood.
The flag may be repeated twice (`-vv`) for displaying debug output.

### Patching Hades

Adjusting `3440` and `1440` with your own resolution:

```bat
hephaistos patch 3440 1440
```

> Note: you can safely repatch multiple times in a row as Hephaistos always patches based on the original files.
> There is no need to restore files in-between.

### Restoring Hades to its pre-Hephaistos state

```bat
hephaistos restore
```

### Patching Hades again after a game update

Every time it receives an update, Hades will automatically revert to its default resolution, and Hephaistos must be reapplied.
Trying to repatch after a game update will be blocked:

```console
> hephaistos patch 3440 1440
ERROR:hephaistos:Hash file mismatch: 'XXX' was modified.
ERROR:hephaistos:Was the game updated? Re-run with '--force' to discard previous backups and re-patch Hades from its current state.
```

Since the game was updated, the previous backups can be safely discarded.
Use `--force` to repatch and create new backups:

```bat
hephaistos patch 3440 1440 --force
```

## Under the hood

By default, Hades uses a fixed 1920x1080 internal resolution (viewport) with anamorphic scaling (i.e. it can only played at 16:9, no matter the display resolution).

To bypass this limitation, Hephaistos patches the game's files with an ad-hoc viewport computed depending on chosen resolution and scaling algorithm:

```console
> hephaistos patch 3440 1440 -v
INFO:hephaistos:Computed patch viewport (2580, 1080) using scaling hor+ from resolution (3440, 1440)
INFO:hephaistos:Patched 'x64/EngineWin64s.dll' with viewport (2580, 1080)
INFO:hephaistos:Patched 'x64Vk/EngineWin64sv.dll' with viewport (2580, 1080)
INFO:hephaistos:Patched 'x86/EngineWin32s.dll' with viewport (2580, 1080)
INFO:hephaistos:Patched 'Content/Game/GUI/AboutScreen.sjson' with viewport (2580, 1080)
...
INFO:hephaistos:Patched 'Content/Game/GUI/ThreeWayDialog.sjson' with viewport (2580, 1080)
INFO:hephaistos:Installed Lua mod 'hephaistos/lua' to 'Content/Mods/Hephaistos'
INFO:hephaistos:Configured 'Content/Mods/Hephaistos/HephaistosConfig.lua' with viewport (2580, 1080)
INFO:hephaistos:Patched 'Content/Scripts/RoomManager.lua' with hook 'Import "../Mods/Hephaistos/Hephaistos.lua"'

> hephaistos patch 3440 1440 -s pixel -v
INFO:hephaistos:Computed patch viewport (3440, 1440) using scaling pixel from resolution (3440, 1440)
...
```

- Backends' engine DLLs are hex patched to expand the resolution and camera viewports.
- Resource SJSON files are patched to resize / move around GUI elements.
- Gameplay Lua scripts are extended with a Lua mod recalculating sizes / positions of GUI elements.

Two algorithms are supported for computing the viewport to patch:

- `hor+` (Hor+ scaling): expand aspect ratio and field of view horizontally, keep vertical height/field of view. This is the default scaling used by Hephaistos and recommended for general usage.
- `pixel` (pixel-based scaling): expand field of view in all directions without applying any scaling, disregarding aspect ratios. This scaling is not recommended for general usage as it presents way more artifacts due to resizing in both directions rather than only horizontally.

While patching, Hephaistos stores file hashes of the patched files and creates a backup of the original files, which allows for:

- Detecting any outside modifications made to the files -- mostly for detecting game updates.
- Detecting if we are repatching a previously patched installation, in which case the original files are used as basis for in-place repatching without an intermediate restore operation.
- Restoring Hades to its pre-patch state if need be.

Everything is stored under the `hephaistos-data` directory.

## Why did you make this, and how did you know what to patch?

I love Hades and am an ultrawide player myself.
I decided to try my hand at modding ultrawide support by decompiling Hades and reverse-engineering the viewport logic just to see if I could, and here we are 😄

See [this blog post](https://nicolas.busseneau.fr/en/blog/2021/04/hades-ultrawide-mod) for more details about Hephaistos' genesis.
