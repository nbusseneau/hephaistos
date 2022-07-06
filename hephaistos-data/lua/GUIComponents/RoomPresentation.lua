local function scaleDeathBlackScreenBackground(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.DeathBackground, Fraction = 10 })
end

local function scaleBlackScreenBackground(params)
  return Hephaistos.MatchAll(params, { Fraction = 10 })
end

local function repositionTimer(params)
  if params.X and params.Y then
    params.X = Hephaistos.RecomputeFixedXFromLeft(params.X)
    params.Y = Hephaistos.RecomputeFixedYFromBottom(params.Y)
  else
    params.OffsetX = Hephaistos.RecomputeFixedXFromLeft(params.OffsetX)
    params.OffsetY = Hephaistos.RecomputeFixedYFromBottom(params.OffsetY)
  end
end

local filterHooks = {
  RunBiomePresentation = {
    SetScale = {
      -- biome map overlay
      BiomeMapOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Id = ScreenAnchors.BiomePresentation, Fraction = 10 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
    Attach = {
      -- biome map offset
      BiomeMapOffset = {
        Filter = function(params)
          return params.DestinationId == ScreenAnchors.RunDepthDisplayAnchor
            and params.OffsetX and params.OffsetY
        end,
        Callback = Hephaistos.RecenterOffsets,
      },
    },
  },
  -- timer animation at start of each biome when using Tight Deadline pact
  BiomeTimeCheckpointPresentation = {
    CreateScreenObstacle = {
      BiomeTimerAnimation = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = 88, Y = 905, Group = "Overlay" })
        end,
        Callback = repositionTimer,
      },
    },
    Move = {
      Foo = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { OffsetX = 88, OffsetY = 930 })
        end,
        Callback = repositionTimer,
      },
    },
  },
  -- death backgrounds
  DeathPresentation = {
    SetScale = {
      DeathBackground = { Filter = scaleDeathBlackScreenBackground, Callback = Hephaistos.Rescale, },
    },
  },
  SurfaceDeathPresentation = {
    SetScale = {
      DeathBackground = { Filter = scaleDeathBlackScreenBackground, Callback = Hephaistos.Rescale, },
    },
  },
  -- various black screen backgrounds
  StartDemoPresentation = {
    SetScale = {
      BlackScreenBackground = { Filter = scaleBlackScreenBackground, Callback = Hephaistos.Rescale, },
    },
  },
  EndDemoPresentation = {
    SetScale = {
      BlackScreenBackground = { Filter = scaleBlackScreenBackground, Callback = Hephaistos.Rescale, },
    },
  },
  ViewPortraitPresentation = {
    SetScale = {
      BlackScreenBackground = { Filter = scaleBlackScreenBackground, Callback = Hephaistos.Rescale, },
    },
  },
  EpilogueScenePresentation = {
    SetScale = {
      BlackScreenBackground = { Filter = scaleBlackScreenBackground, Callback = Hephaistos.Rescale, },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
