-- keepsakes description box
Hephaistos.CreateScreenComponent.ShowAwardMenu = function(params)
  return Hephaistos.MatchAll(params,
    { Name = "BlankObstacle", Group = "Combat_Menu" },
    { Name = "BlankObstacle", Group = "Combat_Menu_Additive" })
  and params.X >= 1325
end

-- keepsakes icons
Hephaistos.CreateKeepsakeIcon.ShowAwardMenu = function(args)
  return true
end
