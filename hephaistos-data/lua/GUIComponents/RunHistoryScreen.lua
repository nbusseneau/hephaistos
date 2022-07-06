local filters = {
  ShowRunHistoryScreen = {
    -- run history overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Fraction = 10 })
      end,
      Action = Hephaistos.Rescale,
    },
    -- run history left/right arrows
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params,
          { Name = "ButtonRunHistoryLeft", X = ScreenCenterX - 520, Y = 310, Scale = 1.0, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu_Overlay2" },
          { Name = "ButtonRunHistoryRight", X = ScreenCenterX + 478, Y = 310, Scale = 1.0, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu_Overlay2" })
      end,
      Action = function(params) params.Y = Hephaistos.RecomputeFixedYFromTop(params.Y) end,
    },
  },
  ShowRunHistory = {
    -- run history pact of punishment and mirror upgrades icons
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params,
        { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray_Backing", Scale = 0.5 },
        { Name = "TraitTrayMetaUpgradeIconButton", Group = "Combat_Menu_TraitTray" })
        and params.X >= 320 and params.Y >= 900
      end,
      Action = Hephaistos.Recenter,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
