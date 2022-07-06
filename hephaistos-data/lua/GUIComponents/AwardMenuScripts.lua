local descriptionStartX = 1325
local descriptionStartY = 75
local levelProgressYOffset = GetLocalizedValue(380, { { Code = "ja", Value = 380 + 18 }, })
local levelProgressYOffset2 = GetLocalizedValue(720, { { Code = "ja", Value = 740 }, })

local filterHooks = {
  ShowAwardMenu = {
    SetScale = {
      -- keepsakes menu overlay
      KeepsakesMenuOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Fraction = 4 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
    CreateScreenComponent = {
      -- keepsakes menu description box + locked keepsakes icons
      KeepsakesMenuDescriptionBoxAndIcons = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY + 340, Group = "Combat_Menu" },
            { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY + levelProgressYOffset, Group = "Combat_Menu" },
            { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY, Group = "Combat_Menu" },
            { Name = "BlankObstacle", X = descriptionStartX + 230, Y = descriptionStartY + levelProgressYOffset2, Group = "Combat_Menu_Additive" },
            { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY, Group = "Combat_Menu" })
            or Hephaistos.MatchAll(params, { Name = "LegendaryKeepsakeLockedButton", Group = "Combat_Menu" })
        end,
        Callback = Hephaistos.Recenter,
      },
      -- keepsakes menu equip/unequip status text
      KeepsakesMenuEquipStatusText = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = ScreenCenterX, Y = 850, Group = "Combat_Menu" })
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
      },
    },
    -- keepsakes menu icons
    CreateKeepsakeIcon = {
      KeepsakesMenuIcons = {
        Callback = function(component, params) Hephaistos.Recenter(params) end,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
