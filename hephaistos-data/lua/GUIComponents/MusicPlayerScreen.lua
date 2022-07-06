local filterHooks = {
  OpenMusicPlayerScreen = {
    SetScale = {
      -- chamber music overlay
      MusicOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Fraction = 4 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
