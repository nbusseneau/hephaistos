local originalCreditSpacing = DeepCopyTable(CreditSpacing)

local toRecenter = {
	"ColumnLeft",
	"ColumnRight",
	"ColumnCenter",
	"CColumnLeft",
	"CColumnRight",
}

for _, value in ipairs(toRecenter) do
	CreditSpacing[value] = Hephaistos.RecomputeFixedXFromCenter(CreditSpacing[value])
end
CreditSpacing.CreditScrollStart = Hephaistos.RecomputeFixedYFromBottom(CreditSpacing.CreditScrollStart)

local function reposition(args)
	-- reposition X if it was dependent on one of the recentered CreditSpacing values
	if args.X then
		local X = args.X
		for _, value in ipairs(toRecenter) do
			if X == originalCreditSpacing[value] then
				args.X = CreditSpacing[value]
				break
			end
		end
	end

	-- reposition Y if iy was dependent on ScreenCenter
	if args.Y and args.Y == Hephaistos.Original.ScreenCenterY then
		args.Y = Hephaistos.ScreenCenterY
	end

	-- reposition CreditLineBuffer if it was dependent on recomputed CreditScrollStart
	if args.CreditLineBuffer and args.CreditLineBuffer == originalCreditSpacing.CreditScrollStart then
		args.CreditLineBuffer = CreditSpacing.CreditScrollStart
	end
end

-- iterate through CreditsData and reposition everything
for _, section in ipairs(CreditsData) do
	for _, params in ipairs(section) do
		reposition(args)
	end
end
