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

local function recenterXCancelFixedY(params)
  params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
  params.Y = Hephaistos.CancelFixedY(params.Y)
end

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
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI" })
        end,
        Callback = recenterXCancelFixedY,
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
        Callback = recenterXCancelFixedY,
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
        end,
        Callback = recenterXCancelFixedY,
      },
      -- call meter charges
      CallMeterCharges = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Name = "BlankObstacle", Group = "Combat_UI", Y = SuperUI.PipY },
            { Name = "BlankObstacle", Group = "Combat_Menu_Additive", Y = SuperUI.PipY })
            and params.X >= SuperUI.PipXStart - CombatUI.FadeDistance.Super
        end,
        Callback = function(params)
          params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
        end,
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
        Callback = recenterXCancelFixedY,
      },
    },
  },
  LoadAmmo = {
    CreateScreenObstacle = {
      -- self-loaded cast / bloodstones UI
      CastBloodstonesUI = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI" })
        end,
        Callback = recenterXCancelFixedY,
      },
    },
  },
  SelfLoadAmmo = {
    CreateScreenObstacle = {
      -- self-loaded cast / bloodstones UI
      CastBloodstonesUI = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI" })
        end,
        Callback = recenterXCancelFixedY,
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
      Traits = {
        Callback = function(params)
          params.OffsetX = Hephaistos.RecomputeFixedXFromCenter(params.OffsetX)
        end,
      },
    },
  },
  TraitUICreateComponent = {
    CreateScreenObstacle = {
      Traits = {
        Callback = function(params)
          params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
        end,
      },
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
      Traits = {
        Callback = function(params)
          params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
        end,
      },
    },
  },
  TraitUIActivateTrait = {
    CreateScreenObstacle = {
      Traits = { Callback = Hephaistos.Recenter, },
    },
  },
  SortPriorityTraits = {
    SpawnObstacle = {
      Traits = {
        Callback = function(params)
          params.OffsetX = Hephaistos.RecomputeFixedXFromCenter(params.OffsetX)
        end,
      },
    },
  },
  -- other traits / frames recentering (non-left side traits)
  ShowAdvancedTooltipScreen = {
    CreateScreenComponent = {
      Traits = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Name = "rectangle01", X = ScreenCenterX, Y = ScreenCenterY, Group = "Combat_UI_Backing" },
            { Name = "ButtonClose", Scale = 0.7, Group = "Combat_Menu_TraitTray" },
            { Group = "Combat_Menu_TraitTray_Backing", X = 160, Y = 200, Scale = 0.5 },
            { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray_Backing", Scale = 0.5, },
            { Name = "TraitTrayMetaUpgradeIconButton", Group = "Combat_Menu_TraitTray" },
            { Group = "Combat_Menu_TraitTray_Backing", X = 160, Y = 910, Scale = 0.5 })
        end,
        Callback = Hephaistos.Recenter,
      },
      MoreTraits = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Name = "TraitTrayIconButton", Group = "Combat_Menu_TraitTray" },
            { Name = "TraitTrayBackground", Group = "Combat_Menu_TraitTray_Backing", X = 450, Y = ScreenHeight / 2 - 118 },
            { Name = "TraitTray_Center", Group = "Combat_Menu_TraitTray_Backing", X = CombatUI.TraitUIStart, Y = 32 + ScreenHeight / 2 - 100 },
            { Name = "TraitTray_Right", Group = "Combat_Menu_TraitTray_Backing", Y = ScreenHeight / 2 - 100 },
            { Name = "TraitTray_ShortColumn", Group = "Combat_Menu_TraitTray_Backing", Y = (TraitUI.IconStartY + 2.5 * TraitUI.SpacerY) - 0 },
            { Name = "TraitTray_LongColumn", Group = "Combat_Menu_TraitTray_Backing", Y = (TraitUI.IconStartY + 2.5 * TraitUI.SpacerY) - 0 })
        end,
        Callback = function(params)
          params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
        end,
      },
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
          return Hephaistos.MatchAll(params,
            { Group = "Combat_Menu_TraitTray_Backing", X = CombatUI.TraitUIStart },
            { Name = "TraitTray_SlotIcon_Attack", Group = "Combat_Menu_TraitTray_Backing", X = TraitUI.IconStartX },
            { Name = "TraitTray_SlotIcon_Secondary", Group = "Combat_Menu_TraitTray_Backing", X = TraitUI.IconStartX },
            { Name = "TraitTray_SlotIcon_Ranged", Group = "Combat_Menu_TraitTray_Backing", X = TraitUI.IconStartX },
            { Name = "TraitTray_SlotIcon_Dash", Group = "Combat_Menu_TraitTray_Backing", X = TraitUI.IconStartX },
            { Name = "TraitTray_SlotIcon_Wrath", Group = "Combat_Menu_TraitTray_Backing", X = TraitUI.IconStartX },
            { Name = "TraitTray_SlotFrame", Group = "Combat_Menu_TraitTray_Backing", X = TraitUI.IconStartX },
            { Name = "TraitTray_KeepsakeBacking", Group = "Combat_Menu_TraitTray_Backing", X = TraitUI.IconStartX })
        end,
        Callback = function(params)
          params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
        end,
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
