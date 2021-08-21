-- boiling blood animation when getting hit by [Redacted] bloodstone
Hephaistos.CreateAnimation[CastEmbeddedPresentationStart] = function(params)
	return Hephaistos.MatchAll(params, { Name = "HadesBloodstoneVignette", DestinationId = ScreenAnchors.HadesBloodstoneVignette })
end

-- poison animation when getting hit by poison
Hephaistos.CreateAnimation[StartStyxPoisonPresentation] = function(params)
	return Hephaistos.MatchAll(params, { Name = "PoisonVignetteLoop", DestinationId = ScreenAnchors.PoisonVignette })
end

-- fire animation when getting hit by lava
Hephaistos.SetAnimation[StartLavaPresentation] = function(params)
	return Hephaistos.MatchAll(params, { Name = "LavaVignetteSpawner", DestinationId = ScreenAnchors.LavaVignette })
end

-- fix full screen alert overlay displace fx
-- for all calls e.g. call, [Redacted] call, Theseus call and Cerberus interaction during [Redacted] fight
local function replaceObstacleAlertFx(params)
  return Hephaistos.MatchAll(params, { Name = "FullscreenAlertDisplace", Group = "FX_Displacement", DestinationId = ScreenAnchors.FullscreenAlertFxAnchor })
end
Hephaistos.SpawnObstacle[DoAssistPresentation] = replaceObstacleAlertFx
Hephaistos.SpawnObstacle[DoHadesAssistPresentation] = replaceObstacleAlertFx
Hephaistos.SpawnObstacle[DoFullSuperPresentation] = replaceObstacleAlertFx
Hephaistos.SpawnObstacle[DoTheseusSuperPresentation] = replaceObstacleAlertFx

local function filterAnimationAlertFx(params)
  return Hephaistos.MatchAll(params, { Name = "LegendaryAspectSnow", DestinationId = ScreenAnchors.FullscreenAlertFxAnchor })
end
Hephaistos.CreateAnimation[DoCerberusAssistPresentation] = filterAnimationAlertFx

-- fix assist/summon overlay
Hephaistos.Teleport[DoAssistPresentation] = function(params)
	return params.OffsetX and params.OffsetY
end
Hephaistos.CreateAnimation[DoAssistPresentation] = function(params)
	return Hephaistos.MatchAll(params,
		{ Name = "WrathPresentationStreak" },
		{ Name = "WrathPresentationBottomDivider" },
		{ Name = "WrathVignette" })
end
