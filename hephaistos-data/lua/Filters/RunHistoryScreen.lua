-- run history meta upgrades (pacts + mirror)
Hephaistos.CreateScreenComponent.ShowRunHistory = function(params)
  return Hephaistos.MatchAll(params,
    { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray_Backing" },
    { Name = "TraitTrayMetaUpgradeIconButton", Group = "Combat_Menu_TraitTray" })
  and params.X >= 320 and params.Y >= 900
end
