-- biome map (world map shown between)
Hephaistos.Attach[RunBiomePresentation] = function(params)
  return params.DestinationId == ScreenAnchors.RunDepthDisplayAnchor
		and params.OffsetX and params.OffsetY
end

-- reroll vignette overlay
local function fixRerollVignette(params)
  return Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = ScreenCenterX, Y = ScreenCenterY, Group = "Combat_Menu_TraitTray" })
end
Hephaistos.CreateScreenObstacle[FullScreenFadeInAnimationReroll] = fixRerollVignette
Hephaistos.CreateScreenObstacle[FullScreenFadeOutAnimationReroll] = fixRerollVignette

-- fix full screen alert overlay displace/color fx
-- for various events e.g. survival encounter, Hades speaking, Chaos interact
local function replaceObstacleAlertFx(params)
  return Hephaistos.MatchAll(params,
    { Group = "FX_Displacement", DestinationId = ScreenAnchors.FullscreenAlertFxAnchor },
    { Group = "FX_Standing_Top", DestinationId = ScreenAnchors.FullscreenAlertFxAnchor },
    { Group = "FX_Add_Top", DestinationId = ScreenAnchors.FullscreenAlertFxAnchor })
end
Hephaistos.SpawnObstacle[SurvivalEncounterStartPresentation] = replaceObstacleAlertFx
Hephaistos.SpawnObstacle[DoHadesSpeakingPresentation] = replaceObstacleAlertFx
Hephaistos.SpawnObstacle[BoonInteractPresentation] = replaceObstacleAlertFx
Hephaistos.SpawnObstacle[WeaponKitSpecialInteractPresentation] = replaceObstacleAlertFx
Hephaistos.SpawnObstacle[LegendaryAspectPresentation] = replaceObstacleAlertFx
Hephaistos.SpawnObstacle[ChaosInteractPresentation] = replaceObstacleAlertFx

local function filterAnimationAlertFx(params)
  return Hephaistos.MatchAll(params, { DestinationId = ScreenAnchors.FullscreenAlertFxAnchor })
end
Hephaistos.CreateAnimation[WeaponKitSpecialInteractPresentation] = filterAnimationAlertFx
Hephaistos.CreateAnimation[LegendaryAspectPresentation] = filterAnimationAlertFx
