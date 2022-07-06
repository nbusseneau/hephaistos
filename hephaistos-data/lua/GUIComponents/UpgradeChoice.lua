local filterHooks = {
  OpenUpgradeChoiceMenu = {
    SetScale = {
      -- boon / hammer choice menu overlay
      UpgradeChoiceMenuOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Id = ScreenAnchors.ChoiceScreen.Components.ShopBackgroundDim.Id, Fraction = 4 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
    CreateScreenComponent = {
      -- top left icon on boon / hammer choice menu
      UpgradeChoiceMenuTopLeftIcon = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu", X = 182, Y = 160 })
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
  CreateBoonLootButtons = {
    CreateScreenComponent = {
      -- the boons themselves
      UpgradeChoiceMenuBoons = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Group = "Combat_Menu" },
            { Group = "Combat_Menu_Overlay_Backing" })
            and params.X and params.Y
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
