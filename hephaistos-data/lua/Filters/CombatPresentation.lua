-- fix assist/summon overlay
Hephaistos.Teleport[DoAssistPresentation] = function(params)
	return params.OffsetX and params.OffsetY
end
