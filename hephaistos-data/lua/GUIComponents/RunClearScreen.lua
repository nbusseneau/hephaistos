-- run clear overlay background
Hephaistos.SetScale[ShowRunClearScreen] = function(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.RunClear.Components.Blackout.Id, Fraction = 10 })
end

local function recenterEverything(params)
  return true
end

local runClearScreenCenteringFilters = {
  -- top-left heat counter recentering
  { Hook = "CreateScreenObstacle", Caller = UpdateActiveShrinePoints, Callback = recenterEverything },
  -- main trait UI recentering (left side traits)
  { Hook = "SpawnObstacle", Caller = ShowTraitUI, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = TraitUICreateComponent, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = TraitUICreateText, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = UpdateTraitNumber, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = UpdateAdditionalTraitHint, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = TraitUIActivateTrait, Callback = recenterEverything },
  -- other traits / frames recentering (non-left side traits)
  { Hook = "CreateScreenComponent", Caller = ShowAdvancedTooltipScreen, Callback = recenterEverything },
  { Hook = "CreateScreenComponent", Caller = PinTraitDetails, Callback = recenterEverything },
  { Hook = "CreateScreenObstacle", Caller = CreatePrimaryBacking, Callback = function(params)
    return not Hephaistos.MatchAll(params, { Group = "Combat_Menu_TraitTray_Backing", X = 960, Y = 1015 })
  end }
}

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
  -- register hooks
  Hephaistos.RegisterFilterHook("CreateScreenObstacle", Hephaistos.Recenter)
  Hephaistos.RegisterFilterHook("SpawnObstacle", Hephaistos.RecenterOffsets)
  for _, args in ipairs(runClearScreenCenteringFilters) do
    Hephaistos[args.Hook][args.Caller] = args.Callback
  end

  -- forcibly redraw UI elements not handled by ShowAdvancedTooltipScreen
  forceReshowNonAdvancedTooltipUI()
end)

Hephaistos.RegisterPreHook("CloseRunClearScreen", function(params)
  -- unregister hooks
  for _, args in ipairs(runClearScreenCenteringFilters) do
    Hephaistos[args.Hook][args.Caller] = nil
  end
  Hephaistos.UnregisterHook("CreateScreenObstacle")
  Hephaistos.UnregisterHook("SpawnObstacle")

  -- forcibly redraw UI elements not handled by ShowAdvancedTooltipScreen
  forceReshowNonAdvancedTooltipUI()
end)
