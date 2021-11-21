local function scaleDeathBlackScreenBackground(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.DeathBackground, Fraction = 10 })
end

local function scaleBlackScreenBackground(params)
  return Hephaistos.MatchAll(params, { Fraction = 10 })
end

local filters = {
  RunBiomePresentation = {
    -- biome map overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Id = ScreenAnchors.BiomePresentation , Fraction = 10 })
      end,
      Action = Hephaistos.Rescale,
    },
    -- fix biome map offset
    {
      Hook = "Attach",
      Filter = function(params)
        return params.DestinationId == ScreenAnchors.RunDepthDisplayAnchor
          and params.OffsetX and params.OffsetY
      end,
      Action = Hephaistos.RecenterOffsets,
    },
  },
  -- death black screen background
  DeathPresentation = {
    { Hook = "SetScale", Filter = scaleDeathBlackScreenBackground, Action = Hephaistos.Rescale, },
  },
  SurfaceDeathPresentation = {
    { Hook = "SetScale", Filter = scaleDeathBlackScreenBackground, Action = Hephaistos.Rescale, },
  },
  -- various black screen backgrounds
  StartDemoPresentation = {
    { Hook = "SetScale", Filter = scaleBlackScreenBackground, Action = Hephaistos.Rescale, },
  },
  EndDemoPresentation = {
    { Hook = "SetScale", Filter = scaleBlackScreenBackground, Action = Hephaistos.Rescale, },
  },
  ViewPortraitPresentation = {
    { Hook = "SetScale", Filter = scaleBlackScreenBackground, Action = Hephaistos.Rescale, },
  },
  EpilogueScenePresentation = {
    { Hook = "SetScale", Filter = scaleBlackScreenBackground, Action = Hephaistos.Rescale, },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
