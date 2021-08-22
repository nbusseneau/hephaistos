-- advanced tooltip screen overlay background
Hephaistos.SetScale[ShowAdvancedTooltipScreen] = function(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.TraitTrayScreen.Components.BackgroundTint.Id, Fraction = 10 })
end
