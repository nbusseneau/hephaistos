local filters = {
  OpenUpgradeChoiceMenu = {
    -- boon / hammer choice menu overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Id = ScreenAnchors.ChoiceScreen.Components.ShopBackgroundDim.Id, Fraction = 4 })
      end,
      Action = Hephaistos.Rescale,
    },
    -- top left icon on boon / hammer choice menu
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu", X = 182, Y = 160 })
      end,
      Action = Hephaistos.Recenter,
    },
  },
  CreateBoonLootButtons = {
    -- the boons themselves
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params,
          { Group = "Combat_Menu" },
          { Group = "Combat_Menu_Overlay_Backing" })
          and params.X and params.Y
      end,
      Action = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
