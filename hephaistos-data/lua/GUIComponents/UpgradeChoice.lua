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
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
