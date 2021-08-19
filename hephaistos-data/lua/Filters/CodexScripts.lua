local chapterSpacing = 225
local chapterX = 480
local chapterY = 205

-- codex chapters
Hephaistos.CreateScreenComponent.CodexUpdateChapters = function(params)
  return Hephaistos.MatchAll(params,
    { Name = "ButtonCodexLeft", X = ScreenCenterX - 999, Y = 260, Group = "Combat_Menu_Overlay" },
    { Name = "ButtonCodexRight", X = ScreenCenterX + 999, Y = 260, Group = "Combat_Menu_Overlay" })
  or Hephaistos.MatchAll(params,
    { Name = "ButtonCodexLeft", Y = chapterY, Scale = 0.8, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu_Overlay" })
    and params.X >= chapterX - CodexUI.ArrowLeftSpacerX
  or Hephaistos.MatchAll(params, { Name = "ButtonCodexRight", Y = chapterY, Scale = 0.8, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu_Overlay" })
    and params.X >= chapterX + CodexUI.ArrowRightSpacerX + (CodexUI.MaxChapters - 1) * chapterSpacing
  or Hephaistos.MatchAll(params, { Name = "ButtonCodexTab", Y = chapterY, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu_Overlay" })
    and params.X >= chapterX
end

-- codex entry
local function filterCodexEntry(params)
  return Hephaistos.MatchAll(params,
    { Name = "BlankObstacle", X = 600, Y = 285, Group = "Combat_Menu_Overlay" },
    { Name = "BlankObstacle", X = 770 + 800, Y = 930, Group = "Combat_Menu_Overlay" },
    { Name = "CodexBoonInfoTextBacking", X = 1450, Y = 930, Group = "Combat_Menu_Overlay" })
  or Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = 670, Scale = 1.0, Group = "Combat_Menu_Overlay" })
    and params.Y >= 616
  or Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = 770, Group = "Combat_Menu_Overlay" })
    and params.Y >= 370
end
Hephaistos.CreateScreenComponent.CodexOpenEntry = filterCodexEntry
Hephaistos.CreateScreenComponent.onPressedFunction = function(params)
  ancestor = Hephaistos.GetCallerName(7)
  return ancestor and ancestor == "OpenCodexScreen" and filterCodexEntry(params)
end

-- codex relationship bar
Hephaistos.CreateScreenComponent.CreateRelationshipBar = function(params)
  return Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = 500, Y = 385, Group = "Combat_Menu_Overlay" })
end
