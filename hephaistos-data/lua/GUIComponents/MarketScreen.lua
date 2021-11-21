local filters = {
  OpenMarketScreen = {
    -- wretched broker overlay background
    {
      Hook = "SetScale",
      Filter = function(params)
        return Hephaistos.MatchAll(params, { Fraction = 4 })
      end,
      Action = Hephaistos.Rescale,
    },
  },
}

Hephaistos.LoadFilters(filters, Hephaistos.Filters)
