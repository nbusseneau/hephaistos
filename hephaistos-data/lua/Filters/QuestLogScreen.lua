-- quest log (fates) descriptions
Hephaistos.CreateScreenComponent.OpenQuestLogScreen = function(params)
  return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_Menu", X = 795, Y = 300 })
end
