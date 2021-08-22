-- game stats overlay background
Hephaistos.SetScale[ShowGameStatsScreen] = function(params)
  return Hephaistos.MatchAll(params, { Fraction = 10 })
end
