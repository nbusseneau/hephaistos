local screen = ScreenData.QuestLog

local filters = {
  OpenQuestLogScreen = {
    -- fated list overlay background
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
        -- fated list description box
        return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_Menu", X = 795, Y = 300 })
        -- fated list up-down scrolls
        or Hephaistos.MatchAll(params,
          { Name = "ButtonCodexUp", X = 430, Y = screen.ItemStartY - screen.EntryYSpacer + 1, Scale = 1.0, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu" },
          { Name = "ButtonCodexDown", X = 430, Y = screen.ItemStartY + ( (screen.EntryYSpacer - 1) * screen.ItemsPerPage + 10), Scale = 1.0, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu" })
      end,
      Action = Hephaistos.Recenter,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
