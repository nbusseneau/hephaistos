local filterHooks = {
  DisplayLocationText = {
    CreateScreenObstacle = {
      -- location text banner
      LocationTextBanner = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = ScreenCenterX, Y = ScreenCenterY - 380 })
        end,
        Callback = function(params)
          if not Hephaistos.CenterHUD then
            params.Y = Hephaistos.CancelFixedY(params.Y)
          end
        end,
      },
    },
  },
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
