-- top left icon on boon choice menu
Hephaistos.CreateScreenComponent[OpenUpgradeChoiceMenu] = function(params)
  return Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu", X = 182, Y = 160 })
end
