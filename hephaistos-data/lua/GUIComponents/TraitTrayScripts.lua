local filters = {
  ShowAdvancedTooltipScreen = {
    -- advanced tooltip screen overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Id = ScreenAnchors.TraitTrayScreen.Components.BackgroundTint.Id, Fraction = 10 })
      end,
      Action = Hephaistos.Rescale,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
