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
