local filterHooks = {
  ShowGameStatsScreen = {
    SetScale = {
      -- game stats menu overlay
      GameStatsMenuOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Fraction = 10 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
