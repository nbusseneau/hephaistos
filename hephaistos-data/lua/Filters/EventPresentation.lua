-- vignettes flashes when getting hit
Hephaistos.CreateAnimation[HeroDamagePresentationThread] = function(params)
	return Hephaistos.MatchAll(params, { Name = "BloodFrame", UseScreenLocation = true, OffsetX = ScreenCenterX, OffsetY = ScreenCenterY, GroupName = "Vignette" })
end

Hephaistos.CreateAnimation[HeroArmorDamagePresentationThread] = function(params)
	return Hephaistos.MatchAll(params, { Name = "BloodFrame", UseScreenLocation = true, OffsetX = ScreenCenterX, OffsetY = ScreenCenterY })
end
