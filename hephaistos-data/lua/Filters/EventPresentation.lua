-- vignette flashes when getting hit
Hephaistos.CreateAnimation[HeroDamagePresentationThread] = function(params)
	return Hephaistos.MatchAll(params, { Name = "BloodFrame", UseScreenLocation = true, OffsetX = ScreenCenterX, OffsetY = ScreenCenterY, GroupName = "Vignette" })
end

Hephaistos.CreateAnimation[HeroArmorDamagePresentationThread] = function(params)
	return Hephaistos.MatchAll(params, { Name = "BloodFrame", UseScreenLocation = true, OffsetX = ScreenCenterX, OffsetY = ScreenCenterY })
end

-- fix full screen alert overlay displace fx
-- for important events such as companion quests (Achilles, Sisyphus, etc.) or hidden aspects reveal
local function filterAnimationAlertFx(params)
  return Hephaistos.MatchAll(params, { Name = "WeaponKitInteractVignette", DestinationId = ScreenAnchors.FullscreenAlertFxAnchor })
end
Hephaistos.CreateAnimation[PowerWordPresentationWorld] = filterAnimationAlertFx

local function replaceObstacleAlertFx(params)
  return Hephaistos.MatchAll(params, { Name = "FullscreenAlertColorInvert", Group = "FX_Add_Top", DestinationId = ScreenAnchors.FullscreenAlertFxAnchor })
end
Hephaistos.SpawnObstacle[PowerWordPresentationWorld] = replaceObstacleAlertFx
