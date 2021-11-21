local offset = { X = 110, Y = BoonInfoScreenData.ButtonStartY }

local filters = {
  ShowBoonInfoScreen = {
    -- boon info overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Id = ScreenAnchors.BoonInfoScreen.Components.ShopBackgroundDim.Id, Fraction = 10 })
      end,
      Action = Hephaistos.Rescale,
    },
  },
  CreateBoonInfoButton = {
    -- boon info buttons (the boons themselves)
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params,
          { Name = "BoonInfoButton", Group = "Combat_Menu_TraitTray_Backing", X = offset.X + 455 },
          { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray", X = offset.X + 20 },
          { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray", X = offset.X + 110, Scale = 0.8 },
          { Name = "BoonInfoTraitFrame", Group = "Combat_Menu_TraitTray", X = offset.X + 90, Scale = 0.8 },
          { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray", X = offset.X + 90, Scale = 0.8 },
          { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray", X = offset.X + 142 })
          and params.Y >= offset.Y
      end,
      Action = Hephaistos.Recenter,
    },
  },
  UpdateBoonInfoButtons = {
    -- boon info buttons (the boons themselves) on page change
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Name = "BoonInfoButton", Group = "Combat_Menu_TraitTray_Backing", X = offset.X + 455 })
        and params.Y >= offset.Y
      end,
      Action = Hephaistos.Recenter,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
