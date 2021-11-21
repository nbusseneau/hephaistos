--[[
The positions for various GUI components or effects are hardcoded all around.
When possible, we first try to reposition elements from SJSON resource files as
doing so is more efficient and more compatible when also using other mods,
however some elements can only be reposition dynamically from Lua code.

For these, we hook onto various functions such as `CreateScreenComponent` or
`CreateMetaUpgradeEntry` and single them out to handle on a case-by-case
basis, filtering as precisely as possible (based on caller function and passed
arguments) to prevent side effects on similar items, and then repositioning
or resizing as desired.

Filters are set up in tables formatted as:

  local filters = {
    CallerFunctionName = {
      {
        Hook = "HookFunctionName",
        Filter = { optional: a function returning `true` or `false` depending on
          arguments to `Hook` to determine if we should execute `Action` or not.
          If `Filter` is not present, the hooking code assumes it should always
          execute `Action` },
        Action = functionToExecute,
      },
      { Hook = "AnotherHookedFunction1", Filter = anotherFilter, Action = anotherConditionalAction, },
      { Hook = "AnotherHookedFunction2", Action = anotherUnconditionalAction, },
    },
    AnotherCallerFunction = {
      { Hook = "AnotherHookedFunction1", Filter = anotherFilter, Action = anotherConditionalAction, },
      { Hook = "AnotherHookedFunction2", Action = anotherUnconditionalAction, },
    },
  }

For example, to hook onto the `SetScale(args)` within the context of
`ShowGameStatsScreen` and execute `Hephaistos.Rescale` but only if
`args.Fraction == 10`:

  local filters = {
    ShowGameStatsScreen = {
      -- game stats overlay background
      {
        Hook = "SetScale",
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Fraction = 10 })
        end,
        Action = Hephaistos.Rescale,
      },
    },
  }

All filters should be consolidated in `Hephaistos.Filters` via:

  Hephaistos.LoadFilters(filters, Hephaistos.Filters)

so that they get loaded all at once via a single call to `RegisterFilters`. This
is necessary due to how the ModUtil compatibility layer registers hooks.
]]

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
