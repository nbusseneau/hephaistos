-- fire animation when getting hit by lava
Hephaistos.SetAnimation[StartLavaPresentation] = function(params)
	return Hephaistos.MatchAll(params, { Name = "LavaVignetteSpawner", DestinationId = ScreenAnchors.LavaVignette })
end
