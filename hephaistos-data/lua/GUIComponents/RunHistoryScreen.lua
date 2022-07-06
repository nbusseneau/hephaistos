local filterHooks = {
  ShowRunHistoryScreen = {
    SetScale = {
      -- run history overlay
      RunHistoryOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Fraction = 10 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
    CreateScreenComponent = {
      -- run history left/right arrows
      RunHistoryArrows = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Name = "ButtonRunHistoryLeft", X = ScreenCenterX - 520, Y = 310, Scale = 1.0, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu_Overlay2" },
            { Name = "ButtonRunHistoryRight", X = ScreenCenterX + 478, Y = 310, Scale = 1.0, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu_Overlay2" })
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromTop(params.Y) end,
      },
    },
  },
  ShowRunHistory = {
    CreateScreenComponent = {
      -- run history pacts of punishment and mirror upgrades icons
      RunHistoryPactsAndMirrorUpgrades = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray_Backing", Scale = 0.5 },
            { Name = "TraitTrayMetaUpgradeIconButton", Group = "Combat_Menu_TraitTray" })
            and params.X >= 320 and params.Y >= 900
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
