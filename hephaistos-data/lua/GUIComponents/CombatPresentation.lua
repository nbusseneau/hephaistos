-- fury kill death overlay background
Hephaistos.SetScale[HarpyKillPresentation] = function(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.DeathBackground, Fraction = 10 })
end

-- assist/summon overlay background
local function scaleAssistDimmerOverlay(params)
  return Hephaistos.MatchAll(params, { Fraction = 10 })
end

Hephaistos.SetScale[DoAssistPresentation] = scaleAssistDimmerOverlay
Hephaistos.SetScale[DoHadesAssistPresentation] = scaleAssistDimmerOverlay

-- fix assist/summon overlay offset
local function recenterAssistOverlay(params)
  return params.OffsetX and params.OffsetY
end

Hephaistos.Teleport[DoAssistPresentation] = recenterAssistOverlay
Hephaistos.Teleport[DoHadesAssistPresentation] = recenterAssistOverlay
Hephaistos.Teleport[DoFullSuperPresentation] = recenterAssistOverlay
