-- biome map overlay background
Hephaistos.SetScale[RunBiomePresentation] = function(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.BiomePresentation , Fraction = 10 })
end

-- fix biome map offset
Hephaistos.Attach[RunBiomePresentation] = function(params)
  return params.DestinationId == ScreenAnchors.RunDepthDisplayAnchor
    and params.OffsetX and params.OffsetY
end

-- first time reward overlay background
Hephaistos.SetScale[FirstTimeRewardPresentation] = function(params)
  return Hephaistos.MatchAll(params, { Fraction = 4 })
end

-- death black screen background
local function scaleDeathBlackScreenBackground(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.DeathBackground, Fraction = 10 })
end

Hephaistos.SetScale[DeathPresentation] = scaleDeathBlackScreenBackground
Hephaistos.SetScale[SurfaceDeathPresentation] = scaleDeathBlackScreenBackground

-- various black screen backgrounds
local function scaleBlackScreenBackground(params)
  return Hephaistos.MatchAll(params, { Fraction = 10 })
end

Hephaistos.SetScale[StartDemoPresentation] = scaleBlackScreenBackground
Hephaistos.SetScale[EndDemoPresentation] = scaleBlackScreenBackground
Hephaistos.SetScale[ViewPortraitPresentation] = scaleBlackScreenBackground
Hephaistos.SetScale[EpilogueScenePresentation] = scaleBlackScreenBackground
