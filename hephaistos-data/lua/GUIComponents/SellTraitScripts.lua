local filterHooks = {
  OpenSellTraitMenu = {
    SetScale = {
      -- pool of purging overlay
      PoolOfPurgingOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Id = ScreenAnchors.SellTraitScreen.Components.ShopBackgroundDim.Id, Fraction = 4 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
  },
  CreateSellButtons = {
    CreateScreenComponent = {
      -- the boons themselves
      PoolOfPurgingBoons = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Group = "Combat_Menu" },
            { Group = "Combat_Menu_Overlay" })
            and params.X and params.Y
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
