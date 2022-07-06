local filters = {
  OpenSellTraitMenu = {
    -- pool of purging overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Id = ScreenAnchors.SellTraitScreen.Components.ShopBackgroundDim.Id, Fraction = 4 })
      end,
      Action = Hephaistos.Rescale,
    },
  },
  CreateSellButtons = {
    -- the boons themselves
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params,
          { Group = "Combat_Menu" },
          { Group = "Combat_Menu_Overlay" })
          and params.X and params.Y
      end,
      Action = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
