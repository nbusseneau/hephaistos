local offset = { X = 110, Y = BoonInfoScreenData.ButtonStartY }

local filterHooks = {
  ShowBoonInfoScreen = {
    SetScale = {
      -- codex boon info menu overlay
      CodexBoonInfoMenuOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Id = ScreenAnchors.BoonInfoScreen.Components.ShopBackgroundDim.Id, Fraction = 10 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
  },
  CreateBoonInfoButton = {
    CreateScreenComponent = {
      -- codex boon info menu buttons (the boons themselves)
      CodexBoonInfoMenuButtons = {
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
        Callback = Hephaistos.Recenter,
      },
    },
  },
  UpdateBoonInfoButtons = {
    CreateScreenComponent = {
      -- codex boon info menu buttons (the boons themselves) on page change
      CodexBoonInfoMenuButtons = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BoonInfoButton", Group = "Combat_Menu_TraitTray_Backing", X = offset.X + 455 })
            and params.Y >= offset.Y
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
