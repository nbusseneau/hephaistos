local categoryTitleX = 480
local screen = ScreenData.GhostAdmin

local filters = {
  OpenGhostAdminScreen = {
    -- house contractor overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Fraction = 4 })
      end,
      Action = Hephaistos.Rescale,
    },
    -- house contractor categories
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Name = "ButtonGhostAdminTab", Y = 245, Scale = 1.0, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu" })
          and params.X >= categoryTitleX
      end,
      Action = Hephaistos.Recenter,
    },
    -- house contractor up-down scrolls
    {
      Hook = "CreateScreenComponent",
      Filter = function(params)
        return Hephaistos.MatchAll(params,
          { Name = "ButtonCodexUp", X = 500, Y = screen.ItemStartY - screen.EntryYSpacer + 75, Scale = 0.75, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu" },
          { Name = "ButtonContractorDown", X = 500, Y = screen.ItemStartY + ( (screen.EntryYSpacer + 1) * screen.ItemsPerPage) - 75, Scale = 0.75, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu" })
      end,
      Action = function(params) params.X = Hephaistos.RecomputeFixedXFromCenter(params.X) end,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
