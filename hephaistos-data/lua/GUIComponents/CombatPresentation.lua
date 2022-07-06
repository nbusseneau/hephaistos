-- assist/summon overlay background
local function scaleAssistDimmerOverlay(params)
  return Hephaistos.MatchAll(params, { Fraction = 10 })
end

-- fix assist/summon overlay offset
local function recenterAssistOverlay(params)
  return params.OffsetX and params.OffsetY
end

local filterHooks = {
  HarpyKillPresentation = {
    SetScale = {
      -- fury kill death overlay
      FuryKillDeathOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Id = ScreenAnchors.DeathBackground, Fraction = 10 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
  },
  DoAssistPresentation = {
    SetScale = {
      -- companion assist dimmer overlay
      CompanionAssistDimmerOverlay = { Filter = scaleAssistDimmerOverlay, Callback = Hephaistos.Rescale, },
    },
    Teleport = {
      -- companion assist overlay
      CompanionAssistOverlay = { Filter = recenterAssistOverlay, Callback = Hephaistos.RecenterOffsets, },
    },
  },
  DoHadesAssistPresentation = {
    SetScale = {
      -- hades call dimmer overlay
      HadesCallDimmerOverlay = { Filter = scaleAssistDimmerOverlay, Callback = Hephaistos.Rescale, },
    },
    Teleport = {
      -- hades call overlay
      HadesCallOverlay = { Filter = recenterAssistOverlay, Callback = Hephaistos.RecenterOffsets, },
    },
  },
  DoFullSuperPresentation = {
    Teleport = {
      -- full call overlay
      ZagreusCallOverlay = { Filter = recenterAssistOverlay, Callback = Hephaistos.RecenterOffsets, },
    },
  },
  StartLavaPresentation = {
    CreateScreenObstacle = {
      -- lava fire animation
      LavaFireAnimation = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Scripting", X = ScreenCenterX, Y = ScreenCenterY })
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
