-- house contractor overlay background
Hephaistos.SetScale[OpenGhostAdminScreen] = function(params)
  return Hephaistos.MatchAll(params, { Fraction = 4 })
end

local categoryTitleX = 480
local screen = ScreenData.GhostAdmin

Hephaistos.CreateScreenComponent[OpenGhostAdminScreen] = function(params)
  -- house contractor categories
  return Hephaistos.MatchAll(params, { Name = "ButtonGhostAdminTab", Y = 245, Scale = 1.0, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu" })
    and params.X >= categoryTitleX
  -- house contractor up-down scrolls
  or Hephaistos.MatchAll(params,
  { Name = "ButtonCodexUp", X = 500, Y = screen.ItemStartY - screen.EntryYSpacer + 75, Scale = 0.75, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu" },
  { Name = "ButtonContractorDown", X = 500, Y = screen.ItemStartY + ( (screen.EntryYSpacer + 1) * screen.ItemsPerPage) - 75, Scale = 0.75, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu" })
end
