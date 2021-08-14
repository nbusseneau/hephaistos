--[[
Recompute a fixed value, i.e. a value that was set at an offset from a reference
point. Used for moving around elements with a fixed size or fixed position.

Examples:

- Recompute X value fixed at an offset of 60 from the center of the screen:
		RecomputeFixedValue(1020, 960, 1296) = 1356
- Recompute Y value fixed at an offset of -80 from the bottom of the screen:
		RecomputeFixedValue(1000, 1080, 1600) = 1520
]]
local function RecomputeFixedValue(originalValue, originalReferencePoint, newReferencePoint)
	offset = originalReferencePoint - originalValue
	return newReferencePoint - offset
end

function Hephaistos.RecomputeFixedXFromCenter(originalValue)
	return RecomputeFixedValue(originalValue, Hephaistos.Original.ScreenCenterX, Hephaistos.ScreenCenterX)
end

function Hephaistos.RecomputeFixedXFromRight(originalValue)
	return RecomputeFixedValue(originalValue, Hephaistos.Original.ScreenWidth, Hephaistos.ScreenWidth)
end

function Hephaistos.RecomputeFixedYFromCenter(originalValue)
	return RecomputeFixedValue(originalValue, Hephaistos.Original.ScreenCenterY, Hephaistos.ScreenCenterY)
end

function Hephaistos.RecomputeFixedYFromBottom(originalValue)
	return RecomputeFixedValue(originalValue, Hephaistos.Original.ScreenHeight, Hephaistos.ScreenHeight)
end
