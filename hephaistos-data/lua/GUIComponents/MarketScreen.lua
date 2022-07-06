local filterHooks = {
  OpenMarketScreen = {
    SetScale = {
      -- wretched broker menu overlay
      WretchedBrokerMenuOverlay = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Fraction = 4 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
