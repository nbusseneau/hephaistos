-- fix biome map (world map shown between)
Hephaistos.Attach[RunBiomePresentation] = function(params)
  return params.DestinationId == ScreenAnchors.RunDepthDisplayAnchor
		and params.OffsetX and params.OffsetY
end

-- fix reroll vignette overlay
local function fixRerollVignette(params)
  return Hephaistos.MatchAll(params, {Name = "BlankObstacle", X = ScreenCenterX, Y = ScreenCenterY, Group = "Combat_Menu_TraitTray" })
end
Hephaistos.CreateScreenObstacle[FullScreenFadeInAnimationReroll] = fixRerollVignette
Hephaistos.CreateScreenObstacle[FullScreenFadeOutAnimationReroll] = fixRerollVignette
