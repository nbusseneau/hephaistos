local filterHooks = {
  OpenMusicPlayerScreen = {
    SetScale = {
      -- music menu overlay
      MusicMenuOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Fraction = 4 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
    CreateScreenComponent = {
      -- music menu items
      MusicMenuItems = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_Menu" })
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
      },
    }
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
