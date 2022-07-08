local function recenterMetaUpgradeEntry(args, iconXValueFilter)
  -- we only want to reposition the first MetaUpgradeEntry IconX position, as
  -- others will be based off the first one
  if args.Screen.IconX == iconXValueFilter then
    args.Screen.IconX = Hephaistos.RecomputeFixedXFromCenter(args.Screen.IconX)
  end
  -- however we do want to reposition all Y positions
  args.OffsetY = Hephaistos.RecomputeFixedYFromCenter(args.OffsetY)
end

local filterHooks = {
  OpenMetaUpgradeMenu = {
    SetScale = {
      -- mirror of night overlay
      MirrorOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Id = ScreenAnchors.LevelUpScreen.Components.ShopBackgroundDim.Id, Fraction = 4 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
    CreateScreenComponent = {
      -- mirror of night mirror shards
      MirrorShards = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Name = "rectangle01", Group = "Combat_Menu", X = 464, Y = 415 },
            { Name = "rectangle01", Group = "Combat_Menu", X = 1446, Y = 415 },
            { Name = "rectangle01", Group = "Combat_Menu", X = 814, Y = 50 },
            { Name = "rectangle01", Group = "Combat_Menu", X = 1096, Y = 50 })
        end,
        Callback = Hephaistos.Recenter,
      },
      -- mirror of night upgrades themselves (texts)
      MirrorUpgrades = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = ScreenCenterX - 40, Group = "Combat_Menu" })
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
      },
    },
    CreateMetaUpgradeEntry = {
      -- mirror of night upgrades themselves (icons + buttons)
      MirrorUpgrades = {
        Filter = function(args)
          return args.Screen.IconX ~= nil
        end,
        Callback = function(args) recenterMetaUpgradeEntry(args, 663) end
      },
    },
  },
  OpenShrineUpgradeMenu = {
    SetScale = {
      -- pact of punishment menu overlay
      PactMenuOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Fraction = 4 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
    CreateScreenComponent = {
      -- pact of punishment menu meter bar
      PactMenuMeterBar = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "ShrineMeterBarFill", Group = "Combat_Menu", X = 550, Y = ScreenCenterY - 90 })
        end,
        Callback = function(params) params.X = Hephaistos.RecomputeFixedXFromCenter(params.X) end,
      },
      -- pact of punishment menu weapon image
      PactMenuWeaponImage = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 250, Y = 470 })
        end,
        Callback = Hephaistos.Recenter,
      },
      -- pacts of punishment themselves (texts)
      PactMenuPacts = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_Menu" })
            and params.X and params.Y and params.X == ScreenCenterX + 280 - 68
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
      },
    },
    CreateMetaUpgradeEntry = {
      -- pacts of punishment themselves (icons + buttons)
      PactMenuPacts = {
        Filter = function(args)
          return args.Screen.IconX ~= nil
        end,
        Callback = function(args) recenterMetaUpgradeEntry(args, 970 - 68) end,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
