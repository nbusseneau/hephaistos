-- weapon upgrade weapon image
Hephaistos.CreateScreenComponent[ShowWeaponUpgradeScreen] = function(params)
  return Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 335, Y = 435 })
end
