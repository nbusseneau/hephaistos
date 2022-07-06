local filterHooks = {
  ShowRunClearScreen = {
    SetScale = {
      -- run clear overlay
      RunClearOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Id = ScreenAnchors.RunClear.Components.Blackout.Id, Fraction = 10 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
