local filters = {
  ShowWeaponUpgradeScreen = {
    -- infernal arms aspects upgrade overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Id = ScreenAnchors.WeaponUpgradeScreen.Components.ShopBackgroundDim.Id, Fraction = 10 })
      end,
      Action = Hephaistos.Rescale,
    },
    -- infernal arms aspects upgrade weapon image
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 335, Y = 435 })
      end,
      Action = Hephaistos.Recenter,
    },
    -- infernal arms themselves
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Group = "Combat_Menu_TraitTray", X = ScreenCenterX + 40 })
      end,
      Action = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
