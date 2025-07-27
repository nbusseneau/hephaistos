# Hephaistos

[![GitHub Actions status](https://img.shields.io/github/actions/workflow/status/nbusseneau/hephaistos/build-release.yaml?branch=main)](https://github.com/nbusseneau/hephaistos/actions/workflows/build-release.yaml?query=branch%3Amain)
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

Hephaistos is stable: many users have been using it for a long time, some even from their very first time on Hades, and nothing major has had to be fixed for a while.
Still, there might be rare quirks on specific setups that haven't been detected yet: you are most welcome to report anything by [opening a new issue](https://github.com/nbusseneau/hephaistos/issues/new) (ideally with screenshots / videos / a save file) and I will definitely have a look and fix it&nbsp;👌

**(Click on items to show details. For example, click on [Install](#install) for installation instructions.)**

<details>
<summary><h1>Issues / FAQ</h1></summary>

**(Click on items to show details)**

<details>
<summary><h3>Black / empty bars on the main menu and other menus in game (e.g. Mirror of Night)</h3></summary>

**Short answer:** Hephaistos cannot resize static assets such as animations / FMVs (e.g. main menu) and most on-screen artwork (e.g. in-game menus, dialogues): they will stay at 16:9 in the center of the screen.

**Longer answer:** These static assets were designed by Supergiant Games with the assumption of a 1920x1080 viewport. If Hephaistos were to resize them to fit the screen, they would either have to be distorted (which would be very ugly) or cut (which loses information and would not work for menus anyway, because there are often buttons on the edges that would be cut). Instead, Hephaistos simply centers them, which is why black bars or empty bars are displayed: Hephaistos cannot "invent" something to display instead 😉

There is one exception to the rule: fullscreen overlays (e.g. red flash when getting hit, dialogue dimming) are resized to fit the whole screen instead of being kept in the center. This is done because fullscreen overlays can be stretched without visual artifacts.

Also of note: there are a few assets that actually extend beyond 1920x1080, so these extra bits will now be displayed since the artwork is centered (e.g. Chaos dialogue, Pact of Punishment menu). This was impossible to tell from the original game (since it was cut at 1920x1080), so you are in fact getting a bit more of Hades artwork when using Hephaistos 😁

</details>

<details>
<summary><h3><code>Windows protected your PC</code> popup when trying to run Hephaistos</h3></summary>

Windows SmartScreen is being extra paranoid because Hephaistos is not an EV-signed executable (this costs money).
To run Hephaistos, click on `More info` in the center of the screen and then `Run anyway`.

Note: if you are a power user, you may want to disable Windows SmartScreen altogether (`Reputation-based protection settings` > turn `Potentially unwanted app blocking` off).

</details>

<details>
<summary><h3>Antivirus software says Hephaistos is a virus</h3></summary>

This is a false positive due to Hephaistos containing hex editing code (required for patching Hades' executables) and using PyInstaller for packaging.
It is common for hex-editing PyInstaller-based programs to get falsely detected by AV software and there is nothing I can do about it (see [here](https://github.com/pyinstaller/pyinstaller/blob/develop/.github/ISSUE_TEMPLATE/antivirus.md)).

All I can do is tell you that if you downloaded Hephaistos from this GitHub repository, you are safe to run it (the Windows build is automatically bundled with PyInstaller and directly uploaded to GitHub by GitHub runners themselves, there is very little chance it was tampered with in any way).
If you don't want to trust `hephaistos.exe`, I would recommend reading the source code and using the Python version yourself.

Another solution I would suggest is to remove your antivirus software and stick with the default Windows Defender antivirus. Unlike in ancient times, Windows does a good job at protecting users nowadays, and it also seems not to falsely detect `hephaistos.exe` as a virus (well, at least in most cases). This will also boost your PC performance because third party AV software is very bad for performance (and there is nothing you can do about it).

</details>

<details>
<summary><h3>I thought Supergiant Games said ultrawide was not possible. Why did they lie?</h3></summary>

This is what Supergiant Games said ([source](https://steamcommunity.com/app/1145360/discussions/0/4436564907312758813#c4436564907314425087)):

> Hades is a 2D game and many aspects of it are built around the 16:9 aspect ratio. We cannot just extend the game viewport to ultrawide resolution without introducing a wide variety of problems.

**Short answer:** Personally, I don't think SGG was lying. I've seen the "wide variety of problems" they are talking about, and I believe they said this because of technical debt in their tool chain that'd be impossible for them address properly in a timely manner (it would cost too much).

**Longer answer:** There were definitely a lot of things of fix, this mod was more involved than the typical ultrawide fix mod. The vast majority of ultrawide fixes are for 3D games where one only needs to remove intentional limitations on viewport / aspect ratio with a hex patch (example: Horizon Zero Dawn), hence why generic solutions such as [SUWSF](https://github.com/PhantomGamers/SUWSF) are very useful. In Hades' case, the UI is very, very elaborate (many different menus, each with their own on-screen artworks and interactions), hence an ad-hoc solution dynamically re-adjusting UI elements was required, resulting in a tremendous amount of additional custom work so that individual UI elements are properly positioned after resizing the viewport.

I can see why SGG would not want to invest in supporting this in an official capacity. As a modder if something's not working perfectly well in the modded resolution I can just say "eh, whatever", whereas a less-than-perfect implementation from SGG might be considered botched by users (and rightfully so: if you state you are supporting a resolution, then of course users will expect it to be supported).

After reverse engineering the thing, it seems to me their UI / UX tool stack (e.g. whatever the artists / designers use to create the HUD) would need a huge refactoring to allow for proper support of arbitrary aspect ratios. Deriving from the fixes I had to do, I'm 99% sure the 16:9 limitation actually exists solely due to how their custom in-house tools happened to evolve over the years (they have been reusing stuff since Bastion), and the fact all their games are limited in a similar way is just a byproduct of this (it's basically technical debt). Assuming they did address it, then on top of that they'd have to have people that actually do test arbitrary aspect ratios, and think about how to handle every edge case, etc.

From a business perspective, it's a trade off between the investment required for such a small user base vs. the need / want to gain respect from this small user base, and I'm not blaming SGG for not doing it considering their resources: it's not a huge AAA, this type of complex technical debt is not free to address (it's actually very costly), and at some point business decisions need to be made.

Also, remember that they stopped active development work on Hades a long while ago. We can always hope that at some point they'll be able to address this technical debt and have their next games support ultrawide officially...! 🤞

</details>

<details>
<summary><h3>Can I get banned for using Hephaistos?</h3></summary>

No. Hades is an offline game and is not tamper-protected on any platform (e.g. no VAC on Steam): you will not get banned.

</details>

<details>
<summary><h3>Do achievements still work when using Hephaistos?</h3></summary>

**Short answer:** Yes. Hades uses client-side achievements (i.e. achievements are managed by the game, not by Steam / Epic Games / Microsoft Store) and Hephaistos does not touch anything achievements-related: achievements still work exactly like in the original game.

**Longer answer:** No matter the platform (Steam, Epic Games, Microsoft Store), achievements can be of 2 types: client (offline checks) or server (online checks).

Client achievements are most common. In this mode, achievements are handled client-side (i.e. by the game), offline. There is no check or anything done by the platform: the client sends a message saying "unlock X achievement on Y game" and platform says "sure". This is why you can use [Steam Achievement Manager](https://github.com/gibbed/SteamAchievementManager) to unlock (and even relock) any client achievement of your choice without any consequences. Client achievements are basically "we don't care if anyone cheats, this is only for fun" achievements.

Server achievements are less common. In this mode, achievements are handled server-side (i.e. by the game server or the platform), online. This makes it harder to cheat achievements because the client does not have direct control over achievement checks. If the client (i.e. the game) is also tamper-protected (e.g. Steam's VAC system), then cheating is extremely hard / impossible. Server achievements are basically "serious" achievements.

Any game (no matter if offline or online) can use any type of achievements (client or server). There can even be a mix of both client and server achievements on the same game. With that said:

- Offline games will almost always use client achievements. It is very rare for offline games to use server achievements.
- Online games will typically either:
  - Use only client achievements (and rarely a few server achievements, usually newer achievements added after release).
  - Use only server achievements (and rarely a few client achievements, usually older legacy achievements added before release).

In any case, the takeaway is that there is no reason any mod would disable achievements on any game without tamper-protection:

- Client achievements should not be disabled by the mod (unless you specifically use a mod that says it does that).
- Server achievements cannot be disabled by the mod, period.

However, if the game does use tamper-protection, then you don't want to use any mod at all (even if the mod actually does nothing) because you'd get flagged just because your game has been modified.

In Hades' case, the game is offline, only uses client achievements, and is not tamper-protected. Hephaistos does not touch anything achievements-related: achievements still work exactly like in the original game, so you may do whatever you want with the achievements including using [Steam Achievement Manager](https://github.com/gibbed/SteamAchievementManager) to unlock / relock all of them if you please.

</details>

<details>
<summary><h3>How can I support Hephaistos? Do you have a Patreon or anything? </h3></summary>

Thank you very much, you're not the first one to ask but I don't want to accept donations.
I would instead suggest you spend the money to gift Hades to someone, or to buy another indie game (may I recommend Hotline Miami? 🤩).

</details>

<details>
<summary><h3>Why is it spelled Hephaistos and not Hephaestus / Hephaestos?</h3></summary>

_Ἥφαιστος_ in Ancient Greek can be [transliterated](https://en.wikipedia.org/wiki/Romanization_of_Greek) closest to _Hḗphaistos_. Apparently this is also the ["chiefly academic"](https://en.wiktionary.org/wiki/Hephaestus#Alternative_forms) term. Anyway it was mostly a little fun for myself :)

</details>

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

- **[⚠️ Python version requirement]** Hephaistos was coded for 3.10 (3.11 will work but with `distutils` deprecation warnings, 3.12 will not work as `distutils` are removed, see [#39](https://github.com/nbusseneau/hephaistos/issues/39)).
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

Type `1` to pick the patch option. Hephaistos will again prompt you for your resolution and preferences, and then patch Hades:

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

## `patch`-specific information

You can safely `patch` and re-`patch` multiple times in a row as Hephaistos always patches based on backups of the original files.
There is no need to use `restore` in-between `patch` calls: `restore` should only be used to rollback to original.

Every time it receives an update, Hades will automatically revert to its original resolution, and Hephaistos must be reapplied.
Trying to re-`patch` after a game update will be blocked as Hephaistos detects something happened outside of its control:

```console
> hephaistos patch 3440 1440
ERROR:hephaistos:Hash file mismatch: 'XXX' was modified.
ERROR:hephaistos:Was the game updated? Re-run with '--force' to discard previous backups and re-patch Hades from its current state.
```

And `status` will confirm this:

```console
> hephaistos status
Hades was patched with Hephaistos, but Hades files were modified. Was the game updated?
```

Since the game was updated, the previous backups can be safely discarded.
Use `--force` to repatch and create new backups:

```bat
hephaistos patch 3440 1440 --force
```

### `--scaling`

`patch` supports the following scaling algorithms: **(Click on items to show details)**

<details>
<summary><code>hor+</code> (Hor+ scaling, default for wider aspect ratios)</summary>

Expand aspect ratio and field of view horizontally, keep vertical height / field of view.
This is the default scaling used by Hephaistos for aspect ratios wider than 16:9 (e.g. 21:9), and recommended for general usage as it strives to keep the experience as close to the original as possible.

![scaling_21-9_vanilla](https://user-images.githubusercontent.com/4659919/178168549-5123c4fd-2d35-4f6a-904c-3112806bafb7.jpg)
![scaling_21-9_hor+](https://user-images.githubusercontent.com/4659919/178168543-66e6d0e3-ecd9-4903-bfd1-20062822a31b.jpg)

</details>

<details>
<summary><code>vert+</code> (Vert+ scaling, default for taller aspect ratios)</summary>

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

### `--hud`

`patch` supports the following HUD resizing modes: **(Click on items to show details)**

<details>
<summary><code>expand</code> (default for most aspect ratios)</summary>

Expand the HUD horizontally and vertically.
Static HUD elements will be repositioned to their intended location for the new screen size, e.g. health indicator will be in the bottom left, resource indicator will be in the bottom right.
This is the default HUD resizing mode used by Hephaistos for 16:10, 21:9, and 32:9, but note that you may want to try out `--hud=center` for 32:9 to see what you prefer.

![hud_21-9-vanilla](https://user-images.githubusercontent.com/4659919/178168394-99b68f49-b391-4fa9-9f5b-89be99981a91.jpg)
![hud_21-9_expand](https://user-images.githubusercontent.com/4659919/178168395-2f730460-a8c8-4d11-8a35-8f3b0c003626.jpg)

</details>

<details>
<summary><code>center</code> (default for 48:9 and wider)</summary>

Keep HUD in the center of the screen with the same size as the original 16:9 HUD.
Screen size will change but HUD will not move, static HUD elements will remain at their default 16:9 position.
This is the default HUD resizing mode used by Hephaistos for 48:9 and wider.

![hud_21-9-vanilla](https://user-images.githubusercontent.com/4659919/178168394-99b68f49-b391-4fa9-9f5b-89be99981a91.jpg)
![hud_21-9_center](https://user-images.githubusercontent.com/4659919/178168396-37eb931d-0158-409c-8e8d-702e37fa5435.jpg)

</details>

### `--no-custom-resolution`

By default, `patch` patches a custom resolution in the [`ProfileX.sjson` configuration file](https://www.pcgamingwiki.com/wiki/Hades#Configuration_file.28s.29_location) by updating its `WindowWidth`/`WindowHeight` and `X`/`Y` values.

This has two advantages:

- Ensure the game runs at the preferred resolution.
  - Useful when inadvertently switching to a wrong resolution from the game settings.
  - Useful when playing Hades on a secondary monitor.
- Allow running the game in windowed mode at a specific size.
  - Useful for choosing your own window size in windowed mode.
  - Useful for spanning the game window over multi-monitor without Eyefinity / Surround.

Neither of these are possible in the vanilla game: only the resolutions from the main display are offered from the game settings and the game window cannot be freely resized.

While not recommended, you may use `--no-custom-resolution` if you wish not to force custom resolution through `ProfileX.sjson`.
This is mostly useful for development purposes.

## Miscellaneous options

### `--hades-dir`

By default, Hephaistos assumes that it has been placed in the `Hades` directory.
If it fails to detect Hades files, it will try to auto-detect `Hades` location from Steam / Epic Games / Heroic configuration files and ask to be relocated.

You may use `--hades-dir` to manually specify where `Hades` is located, e.g. if you want to store Hephaistos and its files in a different location than the `Hades` directory.

### `--no-modimporter`

Hephaistos is compatible with Mod Importer[^modimporter] (>= 1.3.0).
If Hephaistos detects it is available, it will run `modimporter` to register / unregister itself during `patch` and `restore` operations, instead of manually editing `Content\Scripts\RoomManager.lua`.

While not recommended, this can be bypassed with `--no-modimporter`, in which case Hephaistos will not run `modimporter` even if detected.
This is mostly useful for development purposes.

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
