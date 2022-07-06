local filterHooks = {
  RunInterstitialPresentation = {
    SetScale = {
      -- interstitial overlay
      InterstitialOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Fraction = 10 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
