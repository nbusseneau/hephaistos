local categoryTitleX = 480
local screen = ScreenData.GhostAdmin

local filterHooks = {
  OpenGhostAdminScreen = {
    SetScale = {
      -- house contractor menu overlay
      HouseContractorMenuOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Fraction = 4 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
    CreateScreenComponent = {
      -- house contractor menu categories
      HouseContractorMenuCategories = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "ButtonGhostAdminTab", Y = 245, Scale = 1.0, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu" })
            and params.X >= categoryTitleX
        end,
        Callback = Hephaistos.Recenter,
      },
      -- house contractor menu up-down scrolls
      HouseContractorMenuScrolls = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Name = "ButtonCodexUp", X = 500, Y = screen.ItemStartY - screen.EntryYSpacer + 75, Scale = 0.75, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu" },
            { Name = "ButtonContractorDown", X = 500, Y = screen.ItemStartY + ((screen.EntryYSpacer + 1) * screen.ItemsPerPage) - 75, Scale = 0.75, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu" })
        end,
        Callback = function(params) params.X = Hephaistos.RecomputeFixedXFromCenter(params.X) end,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
