-- keepsakes overlay background
Hephaistos.SetScale[ShowAwardMenu] = function(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.AwardMenuScreen.Components.ShopBackgroundDim.Id, Fraction = 4 })
end

local descriptionStartX = 1325
local descriptionStartY = 75
local descriptionTextOffsetX = 0
local descriptionTextOffsetY = 185
local levelProgressYOffset = GetLocalizedValue(380, { { Code = "ja", Value = 380 + 18 }, })

Hephaistos.CreateScreenComponent[ShowAwardMenu] = function(params)
  -- keepsakes description box
  return Hephaistos.MatchAll(params,
    { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY + 340, Group = "Combat_Menu" },
    { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY + levelProgressYOffset, Group = "Combat_Menu" },
    { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY, Group = "Combat_Menu" },
    { Name = "BlankObstacle", X = descriptionStartX + 230, Y = descriptionStartY + GetLocalizedValue(720, { { Code = "ja", Value = 740 }, }), Group = "Combat_Menu_Additive" },
    { Name = "BlankObstacle", X = descriptionStartX, Y = descriptionStartY, Group = "Combat_Menu" })
  -- locked keepsakes icons
  or Hephaistos.MatchAll(params, { Name = "LegendaryKeepsakeLockedButton", Group = "Combat_Menu" })
end

-- keepsakes icons
Hephaistos.CreateKeepsakeIcon[ShowAwardMenu] = function(components, args)
  return true
end
