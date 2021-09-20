# Hephaistos

https://user-images.githubusercontent.com/4659919/131267791-5e71f0e0-4496-4bf1-bc55-ab5e98eccc9a.mp4

CLI tool for patching any resolution in [Supergiant Games' Hades](https://store.steampowered.com/app/1145360/Hades/), primarily targeting ultrawide monitors (21:9, 32:9) and multi-monitor (48:9).
Hephaistos can bypass both pillarboxing and letterboxing, which are the default on non-16:9 resolutions for Hades, and allows using custom resolutions (useful for custom window sizes and multi-monitor without Eyefinity / Surround).

- For trying out Hephaistos right away, see [Install](#install) below.
- For a preview of how Hades looks in 21:9, 32:9 and 48:9, see [Showcase](#showcase).
- For more details about how Hephaistos works, see [Under the hood](#under-the-hood).

# Issues

I have done several runs with Hephaistos and am confident you should not encounter major issues.

Still, you are most welcome to report anything you witness by [opening a new issue](https://github.com/nbusseneau/hephaistos/issues/new) (ideally with screenshots / videos / a save file) and I will definitely have a look and fix it&nbsp;👌

# Showcase

Some 21:9, 32:9 and 48:9 images below. More images can be found over at [Nexus Mods](https://www.nexusmods.com/hades/mods/107?tab=images) and [WSGF](https://www.wsgf.org/dr/hades/en).

## 21:9 (with HUD expanded)

![Tartarus](https://user-images.githubusercontent.com/4659919/131758654-652b8a8f-6bf9-472e-b645-98b257eaf05d.png)
![Athena](https://user-images.githubusercontent.com/4659919/131758678-340cbe57-bc92-473d-9df4-76f0e2b7470d.png)
![Boons](https://user-images.githubusercontent.com/4659919/131758697-05bf94b3-281d-4756-b11a-e1ad0cd19d9b.png)
![Combat](https://user-images.githubusercontent.com/4659919/131758711-257f562f-0730-4ffc-bc7f-6991c76adabe.png)

## 32:9 (with HUD expanded)

![Tartarus_32-9](https://user-images.githubusercontent.com/4659919/131758668-e2ace1db-fefa-4aa8-a1de-d9271eeb5e3e.png)
![Athena_32-9](https://user-images.githubusercontent.com/4659919/131758683-2baf86f6-0214-4748-9e86-8cf3ee7c9e83.png)
![Boons_32-9](https://user-images.githubusercontent.com/4659919/131758698-433ab8d8-0026-4448-8b91-228f896173bc.png)
![Combat_32-9](https://user-images.githubusercontent.com/4659919/131758712-92aca99f-1fd7-41ae-a709-a3c49394d40a.png)

## 48:9 / triple screen (with HUD centered)

![Tartarus_48-9_hud-center](https://user-images.githubusercontent.com/4659919/132792501-fcbcbf9a-5b02-4f2c-a6e3-da90fb7d0393.jpg)
![Athena_48-9_hud-center](https://user-images.githubusercontent.com/4659919/132792617-79dfd680-0102-4564-9944-d33fb2b057b8.jpg)
![Boons_48-9_hud-center](https://user-images.githubusercontent.com/4659919/132792519-9a654a73-d102-4274-a362-3ef620cbe0a1.jpg)
![Combat_48-9_hud-center](https://user-images.githubusercontent.com/4659919/132792528-67f87b47-0bc3-4aec-8db4-91361292cd77.jpg)

# Install

- Download one of:
  - **[Recommended]** Standalone version:
    - Windows: [hephaistos-windows.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-windows.zip)
    - MacOS: [hephaistos-macos.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-macos.zip)
    - Linux: [hephaistos-linux.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-linux.zip)
  - Python version: [hephaistos-python.zip](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos-python.zip)
- Extract the archive. You should get:
  - Windows: `hephaistos.exe` executable.
  - MacOS / Linux: `hephaistos` executable.
  - Python: `hephaistos`, `hephaistos-data` and `sjson` directories.
- Move all extracted files to Hades main directory. Hephaistos must be sitting right next to the default Hades directories:

```
Hades
├── Content
├── x64
├── x64Vk
├── x86
└── hephaistos.exe
```

> ⚠️&nbsp;If you don't know where Hades is, Hephaistos can try to give you a tip by auto-detecting from Steam and Epic Games configuration files:
>
> - Windows: run `hephaistos.exe`
> - MacOS / Linux: run `hephaistos`
> - Python: run `python -m hephaistos`
>
> Note that you still have to move the files to the Hades directory manually before continuing.

Once Hephaistos is placed in the proper directory, you can use it in two ways:

- **[Easy]** Directly run Hephaistos and follow the interactive instructions: see [Interactive mode](#interactive-mode) for detailed help.
- **[Advanced]** Run Hephaistos from the command line: see [CLI usage](#cli-usage) below.

# Interactive mode

- Windows: run `hephaistos.exe`
- MacOS / Linux: run `hephaistos`
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
...
INFO:hephaistos:Installed Lua mod to 'Content\Mods\Hephaistos'
INFO:hephaistos:Patched 'Content\Scripts\RoomManager.lua' with hook 'Import "../Mods/Hephaistos/Hephaistos.lua"'

Press any key to continue...
```

> ⚠️&nbsp;This can take some time depending on your CPU and hard drive, please be patient&nbsp;⏳

Hades binaries are now patched to work with the chosen resolution.
Start the game and try it out for a bit.

Once done, use Hephaistos again, but this time type `2` to pick the restore option:

```
INFO:hephaistos:Restored backups from 'hephaistos-data\backups' to '.'
INFO:hephaistos:Discarded hashes at 'hephaistos-data\hashes'
INFO:hephaistos:Discarded SJSON data at 'hephaistos-data\sjson-data'
INFO:hephaistos:Uninstalled Lua mod from 'Content\Mods\Hephaistos'
```

Hades binaries are now restored to their original state.

Do note that every time it receives an update, Hades will automatically revert to its default resolution, and Hephaistos must be reapplied.
If in doubt, type `3` to pick the status option and check the current Hades / Hephaistos status.

This concludes the tutorial.
I hope you'll enjoy Hephaistos&nbsp;🥳

# CLI usage

- Windows: run `hephaistos.exe -h`
- MacOS / Linux: run `hephaistos -h`
- Python: run `python -m hephaistos -h`

Hephaistos is mostly self-documented via the CLI help.
Run `hephaistos -h` to find the available subcommands (`patch`, `restore`, etc.) which themselves are documented (e.g. `hephaistos patch -h`).

An optional `-v` flag may be passed to print some information about what Hephaistos is doing under the hood.
The flag may be repeated twice (`-vv`) for displaying debug output.

## Patching Hades using Hephaistos

Adjusting `3440` and `1440` with your own resolution:

```bat
hephaistos patch 3440 1440
```

> Note: you can safely repatch multiple times in a row as Hephaistos always patches based on the original files.
> There is no need to restore files in-between.

### HUD

By default, Hephaistos expands the HUD horizontally as wide as possible: left and right side HUD elements will respectively stay fixed on the left and right after resizing.
For 32:9 or wider resolutions, you might want to use `--hud=center` to keep the HUD in the center of the screen with the same width as the original 16:9 HUD.

### Custom resolution

By default, Hephaistos patches a custom resolution which will be the only resolution available in Hades' display settings.
This is has two advantages:

- Force [`ProfileX.sjson` configuration file](https://www.pcgamingwiki.com/wiki/Hades#Configuration_file.28s.29_location) to update its `WindowWidth`/`WindowHeight` and `X`/`Y` values.
  - Useful for users which had inadvertently switched up their resolutions from the game settings.
- Allow running the game in windowed mode at a specific size.
  - Useful for choosing your own window size in windowed mode.
  - Useful for spanning the game window over multi-monitor without Eyefinity / Surround.
  - This was not possible by default as window size is fixed: only the resolutions from the main display are offered from the game settings and the game window cannot be freely resized, even in windowed or borderless windowed mode and even by manually tweaking [`ProfileX.sjson` configuration file](https://www.pcgamingwiki.com/wiki/Hades#Configuration_file.28s.29_location).

Use `--no-custom-resolution` if you wish to keep regular monitor resolution detection.

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

By default, Hades uses a fixed 1920x1080 internal resolution (viewport) with anamorphic scaling (i.e. it can only played at 16:9, no matter the display resolution).

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

Two algorithms are supported for computing the viewport to patch:

- `hor+` (Hor+ scaling): expand aspect ratio and field of view horizontally, keep vertical height / field of view. This is the default scaling used by Hephaistos and recommended for general usage as it strives to keep the experience as close to the original as possible.
- `pixel` (pixel-based scaling): expand field of view in all directions without applying any scaling, disregarding aspect ratios. This scaling is not recommended for general usage as it presents way more artifacts due to resizing in both directions rather than only horizontally, though some users might enjoy the expanded field of view and native assets scaling.

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
