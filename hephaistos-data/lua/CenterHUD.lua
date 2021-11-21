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

Hephaistos.HUDCenteringFilters = {
  -- top-left heat counter recentering
  UpdateActiveShrinePoints = {
    {
      Hook = "CreateScreenObstacle",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray", X = 26, Y = 54 })
      end,
      Action = Hephaistos.Recenter,
    },
  },
  -- health UI
  ShowHealthUI = {
    {
      Hook = "CreateScreenObstacle",
      Filter = function(params)
        return Hephaistos.MatchAll(params,
          { Name = "BlankObstacle", Group = "Combat_UI", X = 10 - CombatUI.FadeDistance.Health, Y = ScreenHeight - 50 },
          { Name = "BlankObstacle", Group = "Combat_UI", X = 44, Y = ScreenHeight - 60, Scale = 0.5 })
      end,
      Action = Hephaistos.Recenter,
    },
  },
  -- death defiance charges
  RecreateLifePips = {
    {
      Hook = "CreateScreenObstacle",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI", Y = ScreenHeight - 95 })
          and params.X >= 70 + 32
      end,
      Action = Hephaistos.Recenter,
    },
  },
  -- call meter bar
  ShowSuperMeter = {
    {
      Hook = "CreateScreenObstacle",
      Filter = function(params)
        return Hephaistos.MatchAll(params,
          { Name = "BlankObstacle", Group = "Combat_UI", X = 10 - CombatUI.FadeDistance.Super, Y = ScreenHeight - 10},
          { Name = "BlankObstacle", Group = "Combat_Menu", X = 10 - CombatUI.FadeDistance.Super, Y = ScreenHeight - 10},
          { Name = "BlankObstacle", X = 10 , Y = ScreenHeight - 10, Group = "Combat_Menu_Additive"})
        or Hephaistos.MatchAll(params,
          { Name = "BlankObstacle", Group = "Combat_UI", Y = SuperUI.PipY },
          { Name = "BlankObstacle", Group = "Combat_Menu_Additive", Y = SuperUI.PipY })
          and params.X >= SuperUI.PipXStart - CombatUI.FadeDistance.Super
      end,
      Action = Hephaistos.Recenter,
    },
  },
  -- cast / bloodstone ammo UI
  ShowAmmoUI = {
    {
      Hook = "CreateScreenObstacle",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI", X = 512, Y = ScreenHeight - 62 })
      end,
      Action = Hephaistos.Recenter,
    },
  },
  -- objective UI
  CreateObjectiveUI = {
    {
      Hook = "CreateScreenObstacle",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI_World", X = 140 })
      end,
      Action = Hephaistos.Recenter,
    },
  },
  -- main trait UI recentering (left side traits)
  ShowTraitUI = {
    { Hook = "SpawnObstacle", Action = Hephaistos.RecenterOffsets, },
  },
  TraitUICreateComponent = {
    { Hook = "CreateScreenObstacle", Action = Hephaistos.Recenter, },
  },
  TraitUICreateText = {
    { Hook = "CreateScreenObstacle", Action = Hephaistos.Recenter, },
  },
  UpdateTraitNumber = {
    { Hook = "CreateScreenObstacle", Action = Hephaistos.Recenter, },
  },
  UpdateAdditionalTraitHint = {
    { Hook = "CreateScreenObstacle", Action = Hephaistos.Recenter, },
  },
  TraitUIActivateTrait = {
    { Hook = "CreateScreenObstacle", Action = Hephaistos.Recenter, },
  },
  SortPriorityTraits = {
    { Hook = "SpawnObstacle", Action = Hephaistos.RecenterOffsets, },
  },
  -- other traits / frames recentering (non-left side traits)
  ShowAdvancedTooltipScreen = {
    { Hook = "CreateScreenComponent", Action = Hephaistos.Recenter, },
  },
  PinTraitDetails = {
    { Hook = "CreateScreenComponent", Action = Hephaistos.Recenter, },
  },
  CreatePrimaryBacking = {
    {
      Hook = "CreateScreenObstacle",
      Filter = function(params)
        return not Hephaistos.MatchAll(params, { Group = "Combat_Menu_TraitTray_Backing", X = 960, Y = 1015 })
      end,
      Action = Hephaistos.Recenter,
    },
  },
}

-- if center HUD mode is set, hooks are registered statically and HUD is
-- centered permanently
if Hephaistos.CenterHUD then
  Hephaistos.LoadFilters(Hephaistos.HUDCenteringFilters, Hephaistos.Filters)
-- if expand HUD mode is set (default), hooks are enabled/disabled dynamically
-- when displaying run clear screen to center HUD temporarily
else
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

  if ModUtil then
    -- When using ModUtil, we must load all filters upfront due to how we use
    -- ModUtil.Context.Env + ModUtil.Path.Wrap so that they are properly
    -- registered. We then disable the filters immediately on load.
    Hephaistos.LoadFilters(Hephaistos.HUDCenteringFilters, Hephaistos.Filters)
    ModUtil.LoadOnce(function()
      Hephaistos.UnregisterFilters(Hephaistos.HUDCenteringFilters)
    end)
  end

  -- register pre- and post- hooks for recentering RunClearScreen dynamically
  Hephaistos.RegisterPreHook("ShowRunClearScreen", function()
    Hephaistos.RegisterFilters(Hephaistos.HUDCenteringFilters)
    forceRedrawNonAdvancedTooltipUI()
  end)

  Hephaistos.RegisterPostHook("CloseRunClearScreen", function()
    Hephaistos.UnregisterFilters(Hephaistos.HUDCenteringFilters)
    forceRedrawNonAdvancedTooltipUI()
  end)
end
