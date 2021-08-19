-- fix biome map (world map shown between)
Hephaistos.Attach[RunBiomePresentation] = function(params)
  return params.DestinationId == ScreenAnchors.RunDepthDisplayAnchor
		and params.OffsetX and params.OffsetY
end
