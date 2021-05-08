# Hephaistos

![screenshot_3840x1600](https://user-images.githubusercontent.com/4659919/119279618-1cf06980-bc2d-11eb-8185-5915cbeda1e4.png)

CLI tool for patching any resolution in [Supergiant Games' Hades](https://store.steampowered.com/app/1145360/Hades/), initially intended as an ultrawide support mod.
It can bypass both pillarboxing and letterboxing, which are the default on non-16:9 resolutions for Hades.

- For trying out Hephaistos, see [Install](#install) below.
- For more details about how Hephaistos works, see [Under the hood](#under-the-hood).

## Video

https://user-images.githubusercontent.com/4659919/119279604-09dd9980-bc2d-11eb-964a-7893a57fe814.mp4

## Limitations

At the moment, Hephaistos only patches the engine, but does not patch the GUI.
Though as you may see from the image and video, this is definitely possible and was already done manually for demonstration purposes.

The intent is for Hephaistos to eventually automatically patch the GUI, just like it already automatically patches the engine.

## Install

- Download one of:
  - [hephaistos.exe](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos.exe) (recommended, standalone Windows executable)
  - [hephaistos.py](https://github.com/nbusseneau/hephaistos/releases/latest/download/hephaistos.py) (if you want to use Python)
- Move file in Hades main directory. If you don't know where it is:
  - Steam: Right-click on game in library > Manage > Browse local files.
    - Defaults to `C:\Program Files\Steam\steamapps\common\Hades` or `C:\Program Files (x86)\Steam\steamapps\common\Hades`.
  - Epic: Launcher does not provide a way to check where game is installed.
    - Defaults to `C:\Program Files\Epic Games\Hades`.
- If you are new to command line tools, see the [Tutorial](#tutorial) for detailed help.
- Otherwise, see [Usage](#usage) below.

## Tutorial

Hephaistos is a command line tool, and needs to be run from a command prompt.
The easiest way to start a command prompt and use Hephaistos is to:
- Browse to the game's installation folder
- Hold `⇧ Shift` and right-click in the directory
- Select `Open PowerShell window here`

First, try to run Hephaistos with `-h` (standing for `--help`) to get more information about the program. Type the following command and press `↵ Enter`:

```bat
./hephaistos -h
```

Then, try the following commands to patch Hades binaries (adjusting `3440` and `1440` with your own resolution):

```bat
./hephaistos patch -h
./hephaistos patch 3440 1440 -v
```

Hades binaries are now patched to work with an ultrawide 3440x1440 resolution.
Start the game and try it out for a bit.

Once done, try to restore the original binaries:

```bat
./hephaistos restore -h
./hephaistos restore -v
```

Hades binaries are now restored to their original state.

This concludes the tutorial, see [Usage](#usage) for more information about Hephaistos.

## Usage

Hephaistos is mostly self-documented via the CLI help.
Run `./hephaistos -h` to find the available subcommands (`patch`, `restore`), which themselves are documented (e.g. `./hephaistos patch -h`).

All operations accept an optional `-v` flag to print information about what Hephaistos is doing under the hood. The flag may be repeated twice (`-vv`) to also include debug output.

### Patching workflow

To patch Hades for the first time (adjusting `3440` and `1440` with your own resolution):

```bat
./hephaistos patch 3440 1440
```

> Note: it is possible to repatch in-place with different parameters as many times as desired, there is no need to restore files in-between.

This will work until the game receives an update, at which point Hades will automatically revert to its default resolution, and Hephaistos must be reapplied.

Patching after a game update will be blocked:

```console
> ./hephaistos patch 3440 1440
ERROR:root:Current file hash does not match previously stored hash -- was the game updated? If yes, re-run with '--force' to invalidate previous backups and re-patch.
```

Use `--force` to force patch, bypassing file hash check and creating new backups:

```bat
./hephaistos patch 3440 1440 --force
```

### Restoring backups

```bat
./hephaistos restore
```

## Under the hood

By default, Hades uses a fixed 1920x1080 internal resolution (viewport) with anamorphic scaling (i.e. it can only played at 16:9, no matter the display resolution).

To bypass this limitation, Hephaistos hex patches all backends' engine DLL in two specific places with an ad-hoc viewport computed depending on chosen resolution and scaling algorithm:

```console
> ./hephaistos patch 3440 1440 -v
INFO:root:Computed patch viewport (2580, 1080) using scaling hor+
INFO:root:Patched x64\EngineWin64s.dll with viewport (2580, 1080)
INFO:root:Patched x64Vk\EngineWin64sv.dll with viewport (2580, 1080)
INFO:root:Patched x86\EngineWin32s.dll with viewport (2580, 1080)

./hephaistos patch 3440 1440 -s pixel -v
INFO:root:Computed patch viewport (3440, 1440) using scaling pixel
...
```

Two algorithms are supported for computing the ad-hoc viewport:

- `hor+` (Hor+ scaling): expand aspect ratio and field of view horizontally, keep vertical height/field of view. This is the default scaling used by Hephaistos.
- `pixel` (pixel-based scaling): expand field of view in all directions without applying any scaling, disregarding aspect ratios. It is currently provided mostly for demonstration purposes, and is not recommended for general usage.

While patching the binaries, Hephaistos stores file hashes of the patched binaries and creates a backup of the original files, which allows for:

- Detecting any modifications to the files made after a patch, mostly for detecting game updates.
- Detecting if we are repatching a previously patched installation, in which case the backup files are used as basis for in-place repatching without an intermediate restore operation.
- Restoring Hades to its pre-patch state if need be.

Everything is stored under the `hephaistos` directory.

## Why did you make this, and how did you know what to patch?

I love Hades and am an ultrawide player myself.
I decided to try my hand at modding ultrawide support by decompiling Hades and reverse-engineering the viewport logic just to see if I could, and here we are 😄

See [this blog post](https://nicolas.busseneau.fr/en/blog/2021/04/hades-ultrawide-mod) for more details about Hephaistos' genesis.
