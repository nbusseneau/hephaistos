--[[
The positions for various GUI components or effects are hardcoded all around.
When possible, we first try to reposition elements from SJSON resource files
from `patchers.py` as doing so is more efficient and more compatible when also
using other mods, however some elements can only be reposition dynamically from
Lua code.

For these, we hook onto various GUI elements drawing functions such as
`CreateScreenComponent` or `CreateMetaUpgradeEntry` and single them out to
handle on a case-by-case basis, filtering as precisely as possible (based on
caller function and passed arguments) to prevent side effects on similar items,
and then repositioning or resizing as desired.

Filter hooks are of this form:

  local filterHooks = {
    CallerFunction1 = {
      HookedFunction1 = {
        FilterHook1 = {
          Filter = filterFunction1,
          Callback = callbackFunction1,
        },
        FilterHook2 = {
          Filter = filterFunction2,
          Callback = callbackFunction2,
        },
      },
      HookedFunction2 = {
        FilterHook1 = {
          Filter = filterFunction1,
          Callback = callbackFunction1,
        },
      },
    },
    ...
  }

For example, to hook onto `SetScale(args)` within the context of
`ShowGameStatsScreen` and execute `Hephaistos.Rescale` but only if
`args.Fraction == 10`:

  local filterHooks = {
    ShowGameStatsScreen = {
      SetScale = {
        ArbitraryHookName = {
          Filter = function(params)
            return Hephaistos.MatchAll(params, { Fraction = 10 })
          end,
          Callback = Hephaistos.Rescale,
        },
      },
    },
  }

Hephaistos' hooking mechanism requires that hooks be consolidated such that a
single register is done (see `Helpers.lua` for more details), hence all filters
should be consolidated in `Hephaistos.FilterHooks` via:

  Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)

so that they get loaded all at once via `HooksRegister.lua`.
]]

-- statically reposition GUI components
Import "../Mods/Hephaistos/GUIComponents/AwardMenuScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/BoonInfoScreenScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/CodexScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/CombatPresentation.lua"
Import "../Mods/Hephaistos/GUIComponents/GameStatsScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/GhostAdminScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/MarketScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/MetaUpgrades.lua"
Import "../Mods/Hephaistos/GUIComponents/MusicPlayerScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/QuestLogScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/RoomPresentation.lua"
Import "../Mods/Hephaistos/GUIComponents/RunClearScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/RunHistoryScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/SellTraitScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/StoreScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/TraitTrayScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/UIPresentation.lua"
Import "../Mods/Hephaistos/GUIComponents/UpgradeChoice.lua"
Import "../Mods/Hephaistos/GUIComponents/WeaponUpgradeScripts.lua"

-- custom logic to dynamically reposition run clear screen when using expand HUD
-- mode or statically reposition HUD when using center HUD mode
Import "../Mods/Hephaistos/CenterHUD.lua"
