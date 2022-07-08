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
  -- trait details
  PinTraitDetails = {
    CreateScreenComponent = {
      TraitsYCentering = { Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end, },
    },
  },
  SetHighlightedTraitFrame = {
    -- trait on hover tooltip
    SetInteractProperty = {
      TraitOnHoverTooltip = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Property = "TooltipOffsetY" })
        end,
        Callback = function(params)
          params.Value = Hephaistos.RecomputeFixedYFromCenter(params.Value)
        end,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
