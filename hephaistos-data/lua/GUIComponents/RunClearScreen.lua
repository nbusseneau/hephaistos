-- run clear overlay background
Hephaistos.SetScale[ShowRunClearScreen] = function(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.RunClear.Components.Blackout.Id, Fraction = 10 })
end
