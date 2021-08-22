-- interstitial overlay background
Hephaistos.SetScale[RunInterstitialPresentation] = function(params)
  return Hephaistos.MatchAll(params, { Fraction = 10 })
end
