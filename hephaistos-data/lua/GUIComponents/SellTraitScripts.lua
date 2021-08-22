-- pool of purging overlay background
Hephaistos.SetScale[OpenSellTraitMenu] = function(params)
  return Hephaistos.MatchAll(params, { Id = ScreenAnchors.SellTraitScreen.Components.ShopBackgroundDim.Id, Fraction = 4 })
end
