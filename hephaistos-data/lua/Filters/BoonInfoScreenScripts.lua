-- boon info buttons (the boons themselves)
local offset = { X = 110, Y = BoonInfoScreenData.ButtonStartY }
Hephaistos.CreateScreenComponent[CreateBoonInfoButton] = function(params)
  return Hephaistos.MatchAll(params,
    { Name = "BoonInfoButton", Group = "Combat_Menu_TraitTray_Backing", X = offset.X + 455 },
    { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray", X = offset.X + 20 },
    { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray", X = offset.X + 110, Scale = 0.8 },
    { Name = "BoonInfoTraitFrame", Group = "Combat_Menu_TraitTray", X = offset.X + 90, Scale = 0.8 },
    { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray", X = offset.X + 90, Scale = 0.8 },
    { Name = "BlankObstacle", Group = "Combat_Menu_TraitTray", X = offset.X + 142 })
    and params.Y >= offset.Y
end

Hephaistos.CreateScreenComponent[UpdateBoonInfoButtons] = function(params)
  return Hephaistos.MatchAll(params, { Name = "BoonInfoButton", Group = "Combat_Menu_TraitTray_Backing", X = offset.X + 455 })
    and params.Y >= offset.Y
end
