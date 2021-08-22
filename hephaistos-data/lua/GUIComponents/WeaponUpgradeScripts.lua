-- infernal arms aspects upgrade overlay background
Hephaistos.SetScale[ShowWeaponUpgradeScreen] = function(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.WeaponUpgradeScreen.Components.ShopBackgroundDim.Id, Fraction = 10 })
end

-- infernal arms aspects upgrade weapon image
Hephaistos.CreateScreenComponent[ShowWeaponUpgradeScreen] = function(params)
  return Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 335, Y = 435 })
end
