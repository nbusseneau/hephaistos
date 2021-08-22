-- boon / hammer choice menu overlay background
Hephaistos.SetScale[OpenUpgradeChoiceMenu] = function(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.ChoiceScreen.Components.ShopBackgroundDim.Id, Fraction = 4 })
end

-- top left icon on boon / hammer choice menu
Hephaistos.CreateScreenComponent[OpenUpgradeChoiceMenu] = function(params)
  return Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu", X = 182, Y = 160 })
end
