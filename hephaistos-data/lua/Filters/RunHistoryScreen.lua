-- run history pact of punishment and mirror upgrades icons
Hephaistos.CreateScreenComponent[ShowRunHistory] = function(params)
  return Hephaistos.MatchAll(params,
    { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray_Backing", Scale = 0.5 },
    { Name = "TraitTrayMetaUpgradeIconButton", Group = "Combat_Menu_TraitTray" })
    and params.X >= 320 and params.Y >= 900
end
