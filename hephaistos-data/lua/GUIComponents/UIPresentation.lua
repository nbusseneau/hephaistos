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
  ShowCodexUpdate = {
    CreateScreenObstacle = {
      -- codex update notification
      CodexUpdateNotification = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = ScreenCenterX, Y = 770, Group = "Combat_UI", })
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromBottom(params.Y) end,
      },
    },
  },
  QuestAddedPresentation = {
    CreateScreenObstacle = {
      -- new fated list quest notification
      NewFatedListQuestNotification = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = ScreenCenterX + 400, Y = 770 })
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromBottom(params.Y) end,
      },
    },
  },
  QuestCompletedPresentation = {
    CreateScreenObstacle = {
      -- completed fated list quest
      CompletedFatedListQuestNotification = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = ScreenCenterX + 400, Y = 770 })
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromBottom(params.Y) end,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
