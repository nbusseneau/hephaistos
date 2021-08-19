-- mirror shards
Hephaistos.CreateScreenComponent[OpenMetaUpgradeMenu] = function(params)
  return Hephaistos.MatchAll(params,
    { Name = "rectangle01", Group = "Combat_Menu", X = 464, Y = 415 },
    { Name = "rectangle01", Group = "Combat_Menu", X = 1446, Y = 415 },
    { Name = "rectangle01", Group = "Combat_Menu", X = 814, Y = 50 },
    { Name = "rectangle01", Group = "Combat_Menu", X = 1096, Y = 50 })
end

Hephaistos.CreateScreenComponent[OpenShrineUpgradeMenu] = function(params)
  -- pact of punishment meter bar
  return Hephaistos.MatchAll(params, { Name = "ShrineMeterBarFill", Group = "Combat_Menu", X = 550, Y = ScreenCenterY - 90 })
  -- pact of punishment weapon image
  or Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 250, Y = 470 })
end

-- mirror upgrade icons
Hephaistos.CreateMetaUpgradeEntry[OpenMetaUpgradeMenu] = function(args)
  return args.Screen.IconX == 663
end

-- pact of punishment icons
Hephaistos.CreateMetaUpgradeEntry[OpenShrineUpgradeMenu] = function(args)
  return args.Screen.IconX == 970 - 68
end
