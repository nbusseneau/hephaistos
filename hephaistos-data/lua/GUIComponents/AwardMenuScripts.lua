-- keepsakes overlay background
Hephaistos.SetScale[ShowAwardMenu] = function(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.AwardMenuScreen.Components.ShopBackgroundDim.Id, Fraction = 4 })
end

-- keepsakes description box
Hephaistos.CreateScreenComponent[ShowAwardMenu] = function(params)
  return Hephaistos.MatchAll(params,
    { Name = "BlankObstacle", Group = "Combat_Menu" },
    { Name = "BlankObstacle", Group = "Combat_Menu_Additive" })
    and params.X >= 1325
  or Hephaistos.MatchAll(params, { Name = "LegendaryKeepsakeLockedButton", Group = "Combat_Menu" })
end

-- keepsakes icons
Hephaistos.CreateKeepsakeIcon[ShowAwardMenu] = function(components, args)
  return true
end
