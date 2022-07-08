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
  -- badge name plate
  CreatePrimaryBacking = {
    CreateScreenObstacle = {
      BadgeNamePlate = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_Menu_Overlay", X = 210, Y = 1052 })
        end,
        Callback = function(params)
          params.X = Hephaistos.RecomputeFixedXFromLeft(params.X)
          params.Y = Hephaistos.RecomputeFixedYFromBottom(params.Y)
        end,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
