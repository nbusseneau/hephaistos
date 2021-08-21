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
