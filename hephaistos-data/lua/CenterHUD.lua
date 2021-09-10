local function recenterEverything(params)
  return true
end

local hudCenteringFilters = {
  -- top-left heat counter recentering
  { Hook = "CreateScreenObstacle", Caller = UpdateActiveShrinePoints, Callback = function(params)
    return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray", X = 26, Y = 54 })
  end },
  -- health UI
  { Hook = "CreateScreenObstacle", Caller = ShowHealthUI, Callback = function(params)
    return Hephaistos.MatchAll(params,
      { Name = "BlankObstacle", Group = "Combat_UI", X = 10 - CombatUI.FadeDistance.Health, Y = ScreenHeight - 50 },
      { Name = "BlankObstacle", Group = "Combat_UI", X = 44, Y = ScreenHeight - 60, Scale = 0.5 })
  end },
  -- death defiance charges
  { Hook = "CreateScreenObstacle", Caller = RecreateLifePips, Callback = function(params)
    return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI", Y = ScreenHeight - 95 })
      and params.X >= 70 + 32
  end },
  -- call meter bar
  { Hook = "CreateScreenObstacle", Caller = ShowSuperMeter, Callback = function(params)
    return Hephaistos.MatchAll(params,
      { Name = "BlankObstacle", Group = "Combat_UI", X = 10 - CombatUI.FadeDistance.Super, Y = ScreenHeight - 10},
      { Name = "BlankObstacle", Group = "Combat_Menu", X = 10 - CombatUI.FadeDistance.Super, Y = ScreenHeight - 10},
      { Name = "BlankObstacle", X = 10 , Y = ScreenHeight - 10, Group = "Combat_Menu_Additive"})
    or Hephaistos.MatchAll(params,
      { Name = "BlankObstacle", Group = "Combat_UI", Y = SuperUI.PipY },
      { Name = "BlankObstacle", Group = "Combat_Menu_Additive", Y = SuperUI.PipY })
      and params.X >= SuperUI.PipXStart - CombatUI.FadeDistance.Super
  end },
  -- cast / bloodstone ammo UI
  { Hook = "CreateScreenObstacle", Caller = ShowAmmoUI, Callback = function(params)
    return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI", X = 512, Y = ScreenHeight - 62 })
  end },
  -- objective UI
  { Hook = "CreateScreenObstacle", Caller = CreateObjectiveUI, Callback = function(params)
    return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_UI_World", X = 140 })
  end },
  -- main trait UI recentering (left side traits)
  { Hook = "SpawnObstacle", Caller = ShowTraitUI, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = TraitUICreateComponent, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = TraitUICreateText, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = UpdateTraitNumber, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = UpdateAdditionalTraitHint, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = TraitUIActivateTrait, Callback = recenterEverything },
  { Hook = "SpawnObstacle", Caller = SortPriorityTraits, Callback = recenterEverything },
  -- other traits / frames recentering (non-left side traits)
  { Hook = "CreateScreenComponent", Caller = ShowAdvancedTooltipScreen, Callback = recenterEverything },
  { Hook = "CreateScreenComponent", Caller = PinTraitDetails, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = CreatePrimaryBacking, Callback = function(params)
    return not Hephaistos.MatchAll(params, { Group = "Combat_Menu_TraitTray_Backing", X = 960, Y = 1015 })
  end },
}

local function registerHooks()
  Hephaistos.RegisterFilterHook("CreateScreenObstacle", Hephaistos.Recenter)
  Hephaistos.RegisterFilterHook("SpawnObstacle", Hephaistos.RecenterOffsets)

  for _, args in ipairs(hudCenteringFilters) do
    Hephaistos[args.Hook][args.Caller] = args.Callback
  end
end

-- if center HUD mode is set, register static hooks and center HUD permanently
if Hephaistos.CenterHUD then
  registerHooks()
-- if expand HUD mode is set (default), register dynamic hooks active only
-- when displaying run clear screen to center HUD temporarily
else
  local function forceReshowNonAdvancedTooltipUI()
    -- heat counter
    HideObstacle({ Id = ScreenAnchors.ShrinePointIconId, Duration = 0.2, IncludeText = true })
    ScreenAnchors.ShrinePointIconId = nil
    UpdateActiveShrinePoints()

    -- main trait UI
    DestroyTraitUI()
    ShowTraitUI()
  end

  Hephaistos.RegisterPreHook("ShowRunClearScreen", function(params)
    registerHooks()

    -- force redraw static UI elements not redrawn by ShowAdvancedTooltipScreen
    forceReshowNonAdvancedTooltipUI()
  end)

  Hephaistos.RegisterPreHook("CloseRunClearScreen", function(params)
    -- unregister hooks
    for _, args in ipairs(hudCenteringFilters) do
      Hephaistos[args.Hook][args.Caller] = nil
    end
    Hephaistos.UnregisterHook("CreateScreenObstacle")
    Hephaistos.UnregisterHook("SpawnObstacle")

    -- force redraw static UI elements not redrawn by ShowAdvancedTooltipScreen
    forceReshowNonAdvancedTooltipUI()
  end)
end
