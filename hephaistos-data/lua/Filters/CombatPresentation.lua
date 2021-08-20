-- poison animation when getting hit by poison
Hephaistos.CreateAnimation[StartLavaPresentation] = function(params)
	return Hephaistos.MatchAll(params, { Name = "PoisonVignetteLoop", DestinationId = ScreenAnchors.PoisonVignette })
end

-- fire animation when getting hit by lava
Hephaistos.SetAnimation[StartLavaPresentation] = function(params)
	return Hephaistos.MatchAll(params, { Name = "LavaVignetteSpawner", DestinationId = ScreenAnchors.LavaVignette })
end
