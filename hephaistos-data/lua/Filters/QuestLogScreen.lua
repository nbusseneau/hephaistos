-- quest log (fates) description box
Hephaistos.CreateScreenComponent[OpenQuestLogScreen] = function(params)
  return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_Menu", X = 795, Y = 300 })
end
