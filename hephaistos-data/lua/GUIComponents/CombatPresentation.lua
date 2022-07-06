-- assist/summon overlay background
local function scaleAssistDimmerOverlay(params)
  return Hephaistos.MatchAll(params, { Fraction = 10 })
end

-- fix assist/summon overlay offset
local function recenterAssistOverlay(params)
  return params.OffsetX and params.OffsetY
end

local filters = {
  HarpyKillPresentation = {
    -- fury kill death overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Id = ScreenAnchors.DeathBackground, Fraction = 10 })
      end,
      Action = Hephaistos.Rescale,
    },
  },
  DoAssistPresentation = {
    { Hook = "SetScale", Filter = scaleAssistDimmerOverlay, Action = Hephaistos.Rescale, },
    { Hook = "Teleport", Filter = recenterAssistOverlay, Action = Hephaistos.RecenterOffsets, },
  },
  DoHadesAssistPresentation = {
    { Hook = "SetScale", Filter = scaleAssistDimmerOverlay, Action = Hephaistos.Rescale, },
    { Hook = "Teleport", Filter = recenterAssistOverlay, Action = Hephaistos.RecenterOffsets, },
  },
  DoFullSuperPresentation = {
    { Hook = "Teleport", Filter = recenterAssistOverlay, Action = Hephaistos.RecenterOffsets, },
  },
  StartLavaPresentation = {
    -- lava fire animation
    {
      Hook = "CreateScreenObstacle",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Scripting", X = ScreenCenterX, Y = ScreenCenterY })
      end,
      Action = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
