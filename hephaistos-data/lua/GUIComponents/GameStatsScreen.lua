local filters = {
  ShowGameStatsScreen = {
    -- game stats overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Fraction = 10 })
      end,
      Action = Hephaistos.Rescale,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
