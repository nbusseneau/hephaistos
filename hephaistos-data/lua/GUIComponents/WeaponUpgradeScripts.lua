local filterHooks = {
  ShowWeaponUpgradeScreen = {
    SetScale = {
      -- infernal arms aspects upgrade overlay
      InfernalArmsMenuOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Id = ScreenAnchors.WeaponUpgradeScreen.Components.ShopBackgroundDim.Id, Fraction = 10 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
    CreateScreenComponent = {
      -- infernal arms aspects upgrade weapon image
      InfernalArmsMenuWeaponImage = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 335, Y = 435 })
        end,
        Callback = Hephaistos.Recenter,
      },
      -- infernal arms aspects themselves
      InfernalArmsMenuAspects = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Group = "Combat_Menu_TraitTray", X = ScreenCenterX + 40 })
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
