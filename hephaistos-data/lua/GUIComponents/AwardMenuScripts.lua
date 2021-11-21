local descriptionStartX = 1325
local descriptionStartY = 75
local levelProgressYOffset = GetLocalizedValue(380, { { Code = "ja", Value = 380 + 18 }, })
local levelProgressYOffset2 = GetLocalizedValue(720, { { Code = "ja", Value = 740 }, })

local filters = {
  ShowAwardMenu = {
    -- keepsakes overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Fraction = 4 })
      end,
      Action = Hephaistos.Rescale,
    },
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return
          -- keepsakes description box
          Hephaistos.MatchAll(params,
            { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY + 340, Group = "Combat_Menu" },
            { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY + levelProgressYOffset, Group = "Combat_Menu" },
            { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY, Group = "Combat_Menu" },
            { Name = "BlankObstacle", X = descriptionStartX + 230, Y = descriptionStartY + levelProgressYOffset2, Group = "Combat_Menu_Additive" },
            { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY, Group = "Combat_Menu" })
          -- locked keepsakes icons
          or Hephaistos.MatchAll(params, { Name = "LegendaryKeepsakeLockedButton", Group = "Combat_Menu" })
      end,
      Action = Hephaistos.Recenter,
    },
    -- keepsakes icons
    { Hook = "CreateKeepsakeIcon", Action = function(component, params) Hephaistos.Recenter(params) end, },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
