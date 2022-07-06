local filterHooks = {
  ShowStoreScreen = {
    SetScale = {
      -- well of charon overlay
      WellOfCharonOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Fraction = 4 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
