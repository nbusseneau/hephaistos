--[[
By default, Hephaistos expands the HUD horizontally as wide as possible. This
is completely fine at 21:9, but at 32:9 it starts to make sense to want the HUD
centered rather than expanded, and at 48:9 this is a necessity.

Also, no matter if we want the HUD centered or not, the run clear screen is
designed for 16:9 and expects the advanced tooltip screen (trait UI) to be
centered.

Depending on Hephaistos configuration, we thus either center the HUD permanently
or dynamically when showing the run clear screen.
]]

Hephaistos.HUDCenteringFilterHooks = {
  UpdateActiveShrinePoints = {
    CreateScreenObstacle = {
      -- top-left heat counter recentering
      TopLeftHeatCounter = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray", X = 26, Y = 54 })
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
  ShowHealthUI = {
    CreateScreenObstacle = {
      -- health UI
      HealthUI = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Name = "BlankObstacle", Group = "Combat_UI", X = 10 - CombatUI.FadeDistance.Health, Y = ScreenHeight - 50 },
            { Name = "BlankObstacle", Group = "Combat_UI", X = 44, Y = ScreenHeight - 60, Scale = 0.5 })
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
  RecreateLifePips = {
    CreateScreenObstacle = {
      -- death defiance charges
      DeathDefianceCharges = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI", Y = ScreenHeight - 95 })
            and params.X >= 70 + 32
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
  ShowSuperMeter = {
    CreateScreenObstacle = {
      -- call meter bar
      CallMeterBar = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Name = "BlankObstacle", Group = "Combat_UI", X = 10 - CombatUI.FadeDistance.Super, Y = ScreenHeight - 10 },
            { Name = "BlankObstacle", Group = "Combat_Menu", X = 10 - CombatUI.FadeDistance.Super, Y = ScreenHeight - 10 },
            { Name = "BlankObstacle", X = 10, Y = ScreenHeight - 10, Group = "Combat_Menu_Additive" })
            or Hephaistos.MatchAll(params,
              { Name = "BlankObstacle", Group = "Combat_UI", Y = SuperUI.PipY },
              { Name = "BlankObstacle", Group = "Combat_Menu_Additive", Y = SuperUI.PipY })
            and params.X >= SuperUI.PipXStart - CombatUI.FadeDistance.Super
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
  ShowAmmoUI = {
    CreateScreenObstacle = {
      -- cast / bloodstones UI
      CastBloodstonesUI = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI", X = 512, Y = ScreenHeight - 62 })
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
  CreateObjectiveUI = {
    CreateScreenObstacle = {
      -- tutorial / objective UI
      TutorialObjectiveUI = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI_World", X = 140 })
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
  -- main trait UI recentering (left side traits)
  ShowTraitUI = {
    SpawnObstacle = {
      Traits = { Callback = Hephaistos.RecenterOffsets, },
    },
  },
  TraitUICreateComponent = {
    CreateScreenObstacle = {
      Traits = { Callback = Hephaistos.Recenter, },
    },
  },
  TraitUICreateText = {
    CreateScreenObstacle = {
      Traits = { Callback = Hephaistos.Recenter, },
    },
  },
  UpdateTraitNumber = {
    CreateScreenObstacle = {
      Traits = { Callback = Hephaistos.Recenter, },
    },
  },
  UpdateAdditionalTraitHint = {
    CreateScreenObstacle = {
      Traits = { Callback = Hephaistos.Recenter, },
    },
  },
  TraitUIActivateTrait = {
    CreateScreenObstacle = {
      Traits = { Callback = Hephaistos.Recenter, },
    },
  },
  SortPriorityTraits = {
    SpawnObstacle = {
      Traits = { Callback = Hephaistos.RecenterOffsets, },
    },
  },
  -- other traits / frames recentering (non-left side traits)
  ShowAdvancedTooltipScreen = {
    CreateScreenComponent = {
      Traits = { Callback = Hephaistos.Recenter, },
    },
  },
  PinTraitDetails = {
    CreateScreenComponent = {
      Traits = { Callback = Hephaistos.Recenter, },
    },
  },
  CreatePrimaryBacking = {
    CreateScreenObstacle = {
      Traits = {
        Filter = function(params)
          return not Hephaistos.MatchAll(params, { Group = "Combat_Menu_TraitTray_Backing", X = 960, Y = 1015 })
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(Hephaistos.HUDCenteringFilterHooks, Hephaistos.FilterHooks)

-- force redraw static UI elements not redrawn by ShowAdvancedTooltipScreen
local function forceRedrawNonAdvancedTooltipUI()
  -- heat counter
  HideObstacle({ Id = ScreenAnchors.ShrinePointIconId, Duration = 0.2, IncludeText = true })
  ScreenAnchors.ShrinePointIconId = nil
  UpdateActiveShrinePoints()

  -- main trait UI
  DestroyTraitUI()
  ShowTraitUI()
end

-- if center HUD mode is set, do nothing
-- HUD centering filter hooks are enabled by default, HUD is centered statically
-- if expand HUD mode is set (default), disable HUD centering filter hooks
-- HUD centering filter hooks are enabled / disabled dynamically when displaying
-- run clear screen to center HUD temporarily
if not Hephaistos.CenterHUD then
  table.insert(Hephaistos.LoadHooks, function() Hephaistos.DisableFilterHooks(Hephaistos.HUDCenteringFilterHooks) end)

  -- register pre- and post- hooks for recentering RunClearScreen dynamically
  Hephaistos.RegisterPreHook("ShowRunClearScreen", function()
    Hephaistos.EnableFilterHooks(Hephaistos.HUDCenteringFilterHooks)
    forceRedrawNonAdvancedTooltipUI()
  end)

  Hephaistos.RegisterPostHook("CloseRunClearScreen", function()
    Hephaistos.DisableFilterHooks(Hephaistos.HUDCenteringFilterHooks)
    forceRedrawNonAdvancedTooltipUI()
  end)
end
