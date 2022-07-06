local function recenterMetaUpgradeEntry(args)
  args.Screen.IconX = Hephaistos.RecomputeFixedXFromCenter(args.Screen.IconX)
  args.OffsetY = Hephaistos.RecomputeFixedYFromCenter(args.OffsetY)
end

local filters = {
  OpenMetaUpgradeMenu = {
    -- mirror of night overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Id = ScreenAnchors.LevelUpScreen.Components.ShopBackgroundDim.Id, Fraction = 4 })
      end,
      Action = Hephaistos.Rescale,
    },
    -- mirror of night mirror shards
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params,
        { Name = "rectangle01", Group = "Combat_Menu", X = 464, Y = 415 },
        { Name = "rectangle01", Group = "Combat_Menu", X = 1446, Y = 415 },
        { Name = "rectangle01", Group = "Combat_Menu", X = 814, Y = 50 },
        { Name = "rectangle01", Group = "Combat_Menu", X = 1096, Y = 50 })
      end,
      Action = Hephaistos.Recenter,
    },
    -- mirror of night upgrades themselves (texts)
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = ScreenCenterX - 40, Group = "Combat_Menu" })
      end,
      Action = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
    },
    -- mirror of night upgrades themselves (icons + buttons)
    {
      Hook = "CreateMetaUpgradeEntry",
      Filter = function(args)
        return args.Screen.IconX == 663
      end,
      Action = recenterMetaUpgradeEntry,
    },
  },
  OpenShrineUpgradeMenu = {
    -- pact of punishment overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Fraction = 4 })
      end,
      Action = Hephaistos.Rescale,
    },
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        -- pact of punishment meter bar
        return Hephaistos.MatchAll(params, { Name = "ShrineMeterBarFill", Group = "Combat_Menu", X = 550, Y = ScreenCenterY - 90 })
        -- pact of punishment weapon image
        or Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 250, Y = 470 })
      end,
      Action = Hephaistos.Recenter,
    },
    -- pact of punishment icons
    {
      Hook = "CreateMetaUpgradeEntry",
      Filter = function(args)
        return args.Screen.IconX == 970 - 68
      end,
      Action = recenterMetaUpgradeEntry,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
