local filterHooks = {
  ShowAdvancedTooltipScreen = {
    -- advanced tooltip screen overlay
    SetScale = {
      AdvancedTooltipScreenOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Id = ScreenAnchors.TraitTrayScreen.Components.BackgroundTint.Id, Fraction = 10 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
